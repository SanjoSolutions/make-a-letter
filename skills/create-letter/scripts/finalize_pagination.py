"""Apply the letter's numbering policy using a current PDF render of the same input.

Requires lxml and pypdf. Render the output again before delivery.
"""
import argparse
import copy
from pathlib import Path
import re
import zipfile
from lxml import etree
from pypdf import PdfReader

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
T = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
S = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'


def finalize(source, rendered_pdf, output):
    source, rendered_pdf, output = map(Path, (source, rendered_pdf, output))
    fmt = source.suffix.lower()
    if fmt not in {'.docx', '.odt'} or output.suffix.lower() != fmt:
        raise ValueError('Input and output must have the same DOCX or ODT format.')
    if output.exists() or output.resolve() in {source.resolve(), rendered_pdf.resolve()}:
        raise ValueError('Choose a new output path; existing files are never overwritten.')
    pages = len(PdfReader(rendered_pdf).pages)
    if pages < 1:
        raise ValueError('The rendered PDF has no pages.')
    changed, found = {}, 0
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    with zipfile.ZipFile(source) as src:
        parts = [n for n in src.namelist() if n.startswith('word/footer') and n.endswith('.xml')] if fmt == '.docx' else ['styles.xml']
        for part in parts:
            root = etree.fromstring(src.read(part), parser)
            candidates = root.iter(f'{{{W}}}p') if fmt == '.docx' else root.xpath('//style:footer//text:p | //style:footer-left//text:p | //style:footer-first//text:p', namespaces={'style': S, 'text': T})
            for p in candidates:
                if fmt == '.docx':
                    instructions = ' '.join(p.xpath('.//w:instrText/text() | .//w:fldSimple/@w:instr', namespaces={'w': W}))
                    text = ''.join(p.xpath('.//w:t/text()', namespaces={'w': W}))
                    numbered = bool(re.search(r'\bPAGE\b', instructions) and re.search(r'\bNUMPAGES\b', instructions))
                else:
                    readable = copy.deepcopy(p)
                    for space in readable.iter(f'{{{T}}}s'):
                        space.text = ' ' * int(space.get(f'{{{T}}}c', '1'))
                    text = ''.join(readable.itertext())
                    numbered = p.find('.//' + f'{{{T}}}page-number') is not None and p.find('.//' + f'{{{T}}}page-count') is not None
                if numbered and 'Seite ' in text and ' von ' in text:
                    found += 1
                    if pages == 1:
                        p.text = None
                        for child in list(p):
                            if child.tag != f'{{{W}}}pPr':
                                p.remove(child)
            if pages == 1:
                changed[part] = etree.tostring(root, encoding='UTF-8', xml_declaration=True)
        if not found:
            raise ValueError('Numbering fields not found. Start from the numbered filled master, not a previously finalized single-page file.')
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, 'w') as dest:
            for info in src.infolist():
                dest.writestr(info, changed.get(info.filename, src.read(info.filename)))
    return {'pages': pages, 'numbering': 'removed' if pages == 1 else 'retained', 'output': str(output)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--rendered-pdf', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        print(finalize(args.input, args.rendered_pdf, args.output))
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        parser.error(str(exc))
