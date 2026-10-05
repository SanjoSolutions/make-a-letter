# Template and field contract

Optimized copy: https://docs.google.com/document/d/1KUpMmpeVk-cPliGhnYhTVDy6gtNYwz6Cl5e4FkeyrkE/edit

Unchanged original: https://docs.google.com/document/d/1xAAGrhdFho0eZIqAjiMKx2Aw_JtSMChmyYrOiGfoHrk/edit

The optimized copy was created and its layout corrected on 2026-10-05. Access can change; verify current permissions when relevant and never change sharing automatically. Bundled `assets/letter-template.docx`, `.odt` and `.pdf` are exports of the corrected optimized copy. PDF is a preview, not a fillable form. Copy assets before editing; never write into the installed plugin.

## Fields

Tokens are `{{KEY}}`; JSON uses `KEY` without braces and string values. All sample identities, contact details, dates and Latin prose were replaced.

| Key | Meaning | Treatment |
| --- | --- | --- |
| ABSENDER | Sender name/organization in return line | Required |
| STRASSE | Sender street/number or postal alternative | Required |
| PLZ_ORT | Sender postal code/town | Required |
| EMPFAENGER | Recipient organization/name/contact | Required; multiple lines allowed |
| EMPF_STRASSE | Recipient street/number or PO box | Required; multiple lines allowed |
| EMPF_ORT | Recipient postal code/town and country if needed | Required; multiple lines allowed |
| IHR_ZEICHEN | Recipient reference | Optional; remove labelled line if empty |
| IHRE_NACHRICHT | Incoming correspondence/date reference | Optional; remove labelled line if empty |
| KONTAKT | Sender's contact person | Optional; distinct from signatory; remove line if empty |
| TELEFON | Sender telephone | Optional; remove line if empty |
| EMAIL | Sender email | Optional; remove line if empty |
| DATUM | Formatted letter date | Required; default domestic format DD.MM.YYYY, e.g. 05.10.2026 |
| BETREFF | Complete subject, including supplied reference when useful | Required; retain bold |
| ANREDE | Full salutation including punctuation | Default: Sehr geehrte Damen und Herren, |
| BRIEFTEXT | Complete letter body | Required; newline creates a paragraph, empty line adds spacing |
| GRUSS | Closing | Default: Mit freundlichen Grüßen |
| UNTERZEICHNER | Signatory below signature space | Required; may differ from ABSENDER/KONTAKT |
| ANLAGEN | Identified attachment names | Optional; newline-separated entries; remove heading and list if empty |

Other fields are single-line. Long values require a rendered fit check. If an address legitimately lacks a required component, adapt that slot with document tools rather than inventing data to satisfy the helper.

## Optional-field cleanup

An absent or whitespace-only optional value means omit its whole field paragraph: label, value or placeholder, and paragraph break. Do not substitute an empty string, a dash, or a blank line for an unknown telephone number. Apply this to the optional reference and contact fields in both native Google Docs and local formats. The bundled local helper already removes these paragraphs; verify equivalent behavior when using other document tools.

Keep the remaining contact lines together in their existing order, without empty paragraphs between Name, Telefon and E-Mail. Preserve one blank separator between populated reference and contact groups and before Datum. If a group is entirely absent, do not leave its field rows or a separator with no group to separate. Keep layout padding, the address-window position and signature space; do not globally delete blank paragraphs.

Example with a contact name and email but no telephone or reference values (the date is illustrative):

```text
Name: Alex Beispiel
E-Mail: alex.beispiel@example.com

Datum: 05.10.2026
```

For Google Docs, identify the field's complete paragraph from a fresh read, then delete its range within the same table cell using current UTF-16 indexes and the actual tab ID. A normal interior paragraph can be removed with its terminating newline. Never delete a table boundary or the cell's required final newline; for a field at that boundary, remove the redundant paragraph by merging within the cell while retaining a valid final paragraph. Preserve or restore the retained paragraph's style if a merge changes it. After edits, read back the information cell and inspect paragraph contents, not just absence of placeholders. Repair leftover empty field paragraphs and check the rendered contact block when available.

## Retained layout

A4 portrait, Form A; margins left 25 mm, right 20 mm, top/bottom 16.9 mm. The initial spacer places the address block near y = 27 mm; the top page margin is not the address-field position. Arial 10 pt normal text and 8 pt return line, single line spacing. The one-row/two-column table retains 100 mm and 75 mm columns with a 45 mm minimum height. The left cell has 20 mm right padding, giving 80 mm usable address width. The right cell has 5 mm top padding and begins at x = 125 mm. Other padding is zero. Its right edge at x = 200 mm is intentional; the body text ends at x = 190 mm.

The return paragraph has 40 pt space below to position the recipient near the top of the Form A recipient zone, y = 44.7–72 mm. Do not copy this gap to recipient paragraphs or remove it as optional whitespace. Keep the return line single-line and validate the final recipient occupies at most six rendered lines within the zone. Never let a long sender line wrap and silently push the recipient down. The subject is bold and followed by two blank lines; salutation/body and body/closing each have one. The signature has three blank lines, followed by the signatory and one blank line before attachments. The master includes a right-aligned footer with automatic page-number and page-count fields. Apply [pagination finalization](pagination.md) to completed letters: remove numbering for one page and retain `Seite x von y` on every page of multipage letters.

A six-line recipient in a two-page Google Docs test rendered at x = 25 mm, with its final line ending near y = 70.5 mm, and both page-number fields updated correctly. A missing telephone/reference test retained adjacent name/email paragraphs and one separator before the date. These are measured examples, not a guarantee for arbitrary content. DOCX/ODT package checks preserve page fields and layout; Word/LibreOffice rendering can differ and must be checked when available. Discover actual tab IDs/ranges before writing.

## Original-template fallback

The original has sender placeholders `<Vorname> <Nachname>`, street and postal fields; recipient samples `Musterempfänger`, `Musterstraße 123`, `12345 Berlin`; reference `zeichen-1234`; phone `+49 123 4567 8901`; email `name@example.com`; date `01.01.2021`; a nested-bracket subject; three Latin body paragraphs; repeated name placeholders; and an empty Anlagen bullet. Replace by role using fresh ranges, distinguishing sender/contact/signatory. Remove all samples before delivery. Preserve its native structure when Google Docs is requested.
