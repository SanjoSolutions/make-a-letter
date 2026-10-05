# Final page numbering

Default for completed letters: one rendered page has no page numbering; two or more pages show `Seite x von y` on every page, including page 1. A user's explicit request overrides this default. This is the chosen plugin behavior, not a claim that DIN forbids numbering one-page letters.

The master templates retain automatic page-number/page-count fields as reusable source material. Their preview may therefore show `Seite 1 von 1`; do not deliver that unchanged for a completed one-page letter. Determine length from the actual completed document's PDF export or an office application's actual pagination. Never guess from word count, input paragraphs, or stored template page counts.

## Google Docs

1. Fill a native copy with its original automatic footer fields intact. Export the finished copy to PDF and read the PDF page count.
2. For one page, read the copy's current footer and delete only the `Seite ` + PAGE_NUMBER + ` von ` + PAGE_COUNT content. Preserve the footer's final paragraph newline and any unrelated footer content. Use the actual footer segment ID, tab ID, current UTF-16 ranges and revision guard. Do not alter the master.
3. For multiple pages, retain the automatic fields on every page. Do not use a different-first-page setting to hide page 1. Verify both the current page and total in the export.
4. Export again after a footer change and verify the count and absence/presence of numbering. Deliver this final export, never the preliminary PDF. Re-evaluate after later wording/layout edits. If an already finalized one-page copy grows, restore automatic page number/count fields via the native Docs UI (the Docs API cannot insert these fields), or refill a fresh copy of the numbered master with the current content. Never put literal page numbers into a shared footer.

## DOCX and ODT

Keep an intermediate filled document with automatic fields. Render it using the available office converter with fields updated. Run:

```text
python <skill-dir>/scripts/finalize_pagination.py --input <workspace>/draft.docx --rendered-pdf <workspace>/draft.pdf --output <outputs>/letter.docx
```

Use matching `.odt` paths for ODT. The PDF must be a current render of that exact filled input; the helper can count PDF pages but cannot establish their provenance. It requires `lxml` and `pypdf`, removes the template's numbering paragraph content for one page, and preserves automatic fields for multiple pages. Other footer paragraphs and body content remain intact. Existing files are never overwritten.

Render the finalized file again, refresh fields and verify its pagination. If the page count crosses the one/multiple-page boundary, repeat from the retained numbered intermediate using the latest measured count. Allow at most three finalization/render passes; disclose instability rather than looping or claiming a pass. For PDF/RTF, export from the finalized editable file and inspect the export too. TXT has no page numbering.

Without a rendering engine or reliable page count, preserve the intermediate automatic fields and label the output as an unverified draft. Explain that single-page suppression is not verified; do not claim the default was applied. On any later edit, rerun finalization from the updated numbered intermediate.
