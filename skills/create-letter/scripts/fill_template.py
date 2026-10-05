"""Fill the bundled DOCX or ODT template without accessing Google Drive.

Usage: python fill_template.py --data letter.json --output letter.docx
Requires lxml. Input is a UTF-8 JSON object keyed by the documented placeholder names.
"""
import argparse
import copy
import json
from pathlib import Path
import re
import zipfile

from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
T = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
TOKEN = re.compile(r'\{\{([A-Z_]+)\}\}')
REQUIRED = {'ABSENDER', 'STRASSE', 'PLZ_ORT', 'EMPFAENGER', 'EMPF_STRASSE',
            'EMPF_ORT', 'DATUM', 'BETREFF', 'BRIEFTEXT', 'UNTERZEICHNER'}
OPTIONAL = {'IHR_ZEICHEN', 'IHRE_NACHRICHT', 'KONTAKT', 'TELEFON', 'EMAIL', 'ANLAGEN'}
DEFAULTS = {'ANREDE': 'Sehr geehrte Damen und Herren,', 'GRUSS': 'Mit freundlichen Grüßen'}
MULTILINE = {'BRIEFTEXT', 'ANLAGEN', 'EMPFAENGER', 'EMPF_STRASSE', 'EMPF_ORT'}


def slots(paragraph, fmt):
    if fmt == 'docx':
        return [(e, 'text') for e in paragraph.iter(f'{{{W}}}t')]
    result = []
    def walk(e):
        if e.text:
            result.append((e, 'text'))
        for child in e:
            walk(child)
            if child.tail:
                result.append((child, 'tail'))
    walk(paragraph)
    return result


def text_of(paragraph, fmt):
    return ''.join(getattr(e, attr) or '' for e, attr in slots(paragraph, fmt))


def replace(paragraph, fmt, values):
    # Match across text runs, retaining run properties and all untouched XML parts.
    original = text_of(paragraph, fmt)
    for match in reversed(list(TOKEN.finditer(original))):
        parts = slots(paragraph, fmt)
        pos = 0
        for e, attr in parts:
            value = getattr(e, attr) or ''
            end = pos + len(value)
            if end > match.start() and pos < match.end():
                left = max(0, match.start() - pos)
                right = min(len(value), match.end() - pos)
                inserted = values[match.group(1)] if pos <= match.start() < end else ''
                setattr(e, attr, value[:left] + inserted + value[right:])
                if fmt == 'docx':
                    e.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            pos = end


def fill(data, output, template=None):
    output = Path(output)
    fmt = output.suffix.lower().lstrip('.')
    if fmt not in {'docx', 'odt'}:
        raise ValueError('Output must be .docx or .odt; convert/export the filled document for PDF.')
    if not isinstance(data, dict):
        raise ValueError('Data must be a JSON object.')
    unknown = set(data) - REQUIRED - OPTIONAL - set(DEFAULTS)
    if unknown:
        raise ValueError('Unknown fields: ' + ', '.join(sorted(unknown)))
    if any(not isinstance(v, str) for v in data.values()):
        raise ValueError('All field values must be strings; use newline-separated attachments.')
    values = {**{k: '' for k in OPTIONAL}, **DEFAULTS, **data}
    missing = [k for k in REQUIRED | set(DEFAULTS) if not values.get(k, '').strip()]
    if missing:
        raise ValueError('Missing required fields: ' + ', '.join(sorted(missing)))
    for k, v in values.items():
        values[k] = v.replace('\r\n', '\n').replace('\r', '\n').strip()
        if TOKEN.search(v):
            raise ValueError(f'Unresolved placeholder in {k}')
        if '\n' in values[k] and k not in MULTILINE:
            raise ValueError(f'{k} must be a single line.')
    template = Path(template) if template else Path(__file__).resolve().parent.parent / 'assets' / f'letter-template.{fmt}'
    if output.resolve() == template.resolve() or output.exists():
        raise ValueError('Choose a new output file; the template and existing files are never overwritten.')
    part = 'word/document.xml' if fmt == 'docx' else 'content.xml'
    parser = etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False)
    with zipfile.ZipFile(template) as source:
        root = etree.fromstring(source.read(part), parser)
        paragraphs = list(root.iter(f'{{{W}}}p' if fmt == 'docx' else f'{{{T}}}p'))
        observed = set(TOKEN.findall(''.join(text_of(p, fmt) for p in paragraphs)))
        expected = REQUIRED | OPTIONAL | set(DEFAULTS)
        if observed != expected:
            raise ValueError(f'Template field mismatch: missing={expected-observed}, extra={observed-expected}')
        # Track only the information cell; address/signature whitespace is intentional.
        cell_tag = f'{{{W}}}tc' if fmt == 'docx' else '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}table-cell'
        info_cells = [cell for cell in root.iter(cell_tag)
                      if '{{DATUM}}' in ''.join(text_of(p, fmt) for p in cell.iter(f'{{{W if fmt == "docx" else T}}}p'))]
        for p in paragraphs:
            text = text_of(p, fmt)
            matches = list(TOKEN.finditer(text))
            if not values['ANLAGEN'] and text.strip() == 'Anlagen':
                p.getparent().remove(p)
                continue
            if len(matches) == 1 and matches[0].group(1) in OPTIONAL and not values[matches[0].group(1)]:
                p.getparent().remove(p)
                continue
            standalone = TOKEN.fullmatch(text.strip())
            if standalone and standalone.group(1) in MULTILINE:
                key = standalone.group(1)
                lines = values[key].split('\n')
                if key == 'ANLAGEN':
                    lines = [line for line in lines if line.strip()]
                parent = p.getparent()
                anchor = parent.index(p)
                item_anchor = parent.getparent().index(parent) if fmt == 'odt' and key == 'ANLAGEN' and parent.tag == f'{{{T}}}list-item' else None
                for offset, line in enumerate(lines):
                    node = copy.deepcopy(p)
                    replace(node, fmt, {**values, key: line})
                    # ODT list paragraphs need distinct list items, not one item with many paragraphs.
                    if fmt == 'odt' and key == 'ANLAGEN' and parent.tag == f'{{{T}}}list-item':
                        item = copy.deepcopy(parent)
                        for child in list(item):
                            item.remove(child)
                        item.append(node)
                        parent.getparent().insert(item_anchor + offset, item)
                    else:
                        parent.insert(anchor + offset, node)
                if fmt == 'odt' and key == 'ANLAGEN' and parent.tag == f'{{{T}}}list-item':
                    parent.getparent().remove(parent)
                else:
                    parent.remove(p)
            else:
                replace(p, fmt, values)
        # Omitted reference/contact groups must not leave leading or duplicate separators.
        p_tag = f'{{{W if fmt == "docx" else T}}}p'
        for cell in info_cells:
            previous_blank = True
            for p in list(cell):
                if p.tag != p_tag:
                    continue
                blank = not text_of(p, fmt).strip()
                if blank and previous_blank:
                    cell.remove(p)
                else:
                    previous_blank = blank
        # Remove emptied ODT list containers left by an omitted attachments field.
        if fmt == 'odt':
            for tag in ('list-item', 'list'):
                for node in list(root.iter(f'{{{T}}}{tag}')):
                    if not len(node) and not (node.text or '').strip():
                        node.getparent().remove(node)
        if TOKEN.search(''.join(root.itertext())):
            raise ValueError('Unresolved template fields remain.')
        content = etree.tostring(root, encoding='UTF-8', xml_declaration=True)
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, 'w') as dest:
            for info in source.infolist():
                dest.writestr(info, content if info.filename == part else source.read(info.filename))
    return output


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--template')
    args = p.parse_args()
    try:
        print(fill(json.loads(Path(args.data).read_text(encoding='utf-8-sig')), args.output, args.template))
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        p.error(str(exc))
