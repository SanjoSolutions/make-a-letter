# Local formats and export

DOCX and ODT assets were exported from the optimized Google Doc. Use the matching asset directly; local filling needs Python and `lxml`, with no Drive connection. Prefer the host's bundled runtime. Create a UTF-8 JSON object using keys from [template.md](template.md), then run:

```text
python <skill-dir>/scripts/fill_template.py --data <workspace>/letter.json --output <outputs>/letter.docx
python <skill-dir>/scripts/fill_template.py --data <workspace>/letter.json --output <outputs>/letter.odt
```

The helper refuses missing required fields, unknown keys, unresolved tokens, unsupported extensions and overwriting existing files. It edits the main content XML while preserving other package parts, handles tokens split across runs and expands multiline fields into paragraphs. It removes empty optional lines and an unused attachment section. It neither renders documents nor establishes DIN compliance. For a different user-supplied template, inspect its real structure and adapt with document tools instead.

| Output | Local path | Google Drive export MIME type |
| --- | --- | --- |
| DOCX | Fill bundled DOCX | application/vnd.openxmlformats-officedocument.wordprocessingml.document |
| ODT | Fill bundled ODT | application/vnd.oasis.opendocument.text |
| PDF | Render completed DOCX/ODT with supported office converter | application/pdf |
| RTF | Convert completed DOCX/ODT with supported office converter | application/rtf |
| TXT | Write completed text as UTF-8; no page geometry | text/plain |

For PDF/RTF, check converter availability; prefer the bundled office runtime. Do not silently use the user's desktop app. If conversion is unavailable, keep the completed editable file and explain the limit; offer authorized Drive conversion or manual Save as PDF. Never substitute the blank preview PDF for a completed letter or rename an extension as conversion.

For a user-authorized cloud route, fill a native copy first, read its metadata, and export that completed document by its actual ID. Materialize the authenticated returned reference to outputs; do not expose signed download URLs or inline base64. Drive export has a 10 MB limit; follow current Drive guidance for larger files. Do not upload private letter content to bypass a local limitation without authorization.

Reopen DOCX/ODT and check all text, no remaining `{{...}}`, paragraph order, optional-field omission and retained page/style parts. Follow [pagination finalization](pagination.md) after rendering: remove numbering for one-page letters and retain automatic numbering on all pages of longer letters. Render the finalized file again before PDF/RTF export or delivery. Check address fit, subject, signature grouping, clipping and stray pages. Google PDF export does not prove identical Word/LibreOffice pagination. If rendering is unavailable, disclose it and deliver only an unverified draft; do not claim a visual or pagination pass. The bundled template PDF is a reference preview, not an interactive form.
