# Make a letter

Create German letters from a template which follows DIN 5008 norms as local DOCX, ODT or exported PDF, RTF and text, or as a Google Doc.

**Author:** Jonas Aschenbrenner. This repository was prepared and published by Codex at the author's request. The instructions, scripts and documentation were developed with Codex assistance.

[Website](https://make-a-letter.jonas-aschenbrenner.chatgpt.site/) · [Support](https://make-a-letter.jonas-aschenbrenner.chatgpt.site/support/) · [Privacy](https://make-a-letter.jonas-aschenbrenner.chatgpt.site/privacy/) · [Terms](https://make-a-letter.jonas-aschenbrenner.chatgpt.site/terms/)

## What it does

- Drafts a German letter from facts, notes or an existing draft.
- Fills distinct sender, recipient, reference, contact and signature fields.
- Removes unused optional fields, including their empty paragraphs.
- Uses bundled DOCX and ODT templates for local files.
- Supports native Google Docs copies through a separately installed and connected Google Drive plugin.
- Omits numbering for one-page letters and retains automatic “Seite x von y” fields for multipage letters after measuring actual pagination.

The template is based on DIN 5008 norms. It is not DIN certification or a guarantee that an arbitrary finished letter conforms to the standard.

## Use the plugin

Load the repository through your host's supported local-plugin workflow. The root `plugin.json` uses the Agent Plugins format; `.codex-plugin/plugin.json` is a compatibility manifest. The skill is `skills/create-letter/SKILL.md`.

Example prompts:

> Hilf mir, einen Brief zu erstellen. Frage nach den noch fehlenden Angaben.

> Formuliere aus meinen Stichpunkten einen sachlichen Brief und erstelle ihn als DOCX.

> Übertrage meinen Briefentwurf in die Vorlage und prüfe die Platzhalter und das Layout.

Google Docs requires a separately installed and connected Google Drive plugin and access to the source template. No Google Drive integration or MCP server is bundled. Local DOCX/ODT creation does not require Google Drive. PDF and RTF need an available converter or an authorized Google Drive export. Plain text has no page geometry.

The public marketplace submission is being prepared. This repository is source code, not evidence of marketplace approval. Version 0.2.8 is prepared as a skills-only marketplace package with no `.app.json` binding. Publisher verification, portal checks and approval remain separate requirements.

## Run the local helpers

Requirements: Python 3, `lxml`, and `pypdf`. A document renderer such as an office application is needed to verify pagination and export PDF/RTF. The helpers do not render documents themselves.

```sh
python -m pip install lxml pypdf
python skills/create-letter/scripts/fill_template.py --help
python skills/create-letter/scripts/finalize_pagination.py --help
```

Read [the field contract](skills/create-letter/references/template.md), [local format instructions](skills/create-letter/references/local-formats.md), and [pagination finalization](skills/create-letter/references/pagination.md) before generating a letter. Work on copies of the bundled templates. Keep personal letter data outside this repository.

Keep a numbered intermediate, render it to PDF, and finalize the output using the actual page count:

```sh
python skills/create-letter/scripts/finalize_pagination.py \
  --input draft.docx --rendered-pdf draft.pdf --output letter.docx
```

The PDF must be a current render of that exact input. Render and inspect the finalized file again. The helper cannot prove that the PDF and editable file correspond, and an already stripped one-page document needs its numbering restored if later edits make it longer.

## Validation and limits

Development checks covered Google Docs one-page and two-page exports, missing optional fields, and DOCX/ODT footer preservation/removal. Local Word/LibreOffice visual rendering was not verified in the development environment. Always inspect the final document in the application used for delivery.

The plugin does not send correspondence or operate a publisher-run backend. Support email handling is described in the privacy policy.

## Repository contents

`skills/create-letter/assets/` contains the template files; `scripts/` contains the local helpers; `references/` contains field, format and layout instructions. The bundled PDF is a template preview, not a fillable form.

## Licensing

No open-source license has been selected for this repository. Public availability alone does not grant an open-source license. Contact the author about reuse permissions.
