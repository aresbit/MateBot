---
name: x2md-skill
description: Batch convert a directory of slides and PDFs into Markdown. Supports ppt/pptx/pps/ppsx/odp to pdf+md, and text-based pdf to md (no OCR).
---

# X2MD Skill

Use this skill when the user wants batch conversion to Markdown from common document formats.

## What this skill does

- Converts slide files to PDF with LibreOffice (`soffice --headless`)
- Extracts slide text and notes to Markdown from PPTX
- Extracts text from PDF to Markdown (text PDFs only, no OCR)
- Handles mixed extensions in one directory: `.ppt`, `.pptx`, `.pps`, `.ppsx`, `.odp`, `.pdf`
- Mirrors source directory structure in output

## Required toolchain

- Python 3.9+
- `python-pptx` (`pip install python-pptx`)
- `pypdf` (`pip install pypdf`)
- LibreOffice CLI (`soffice` in PATH)

## Run

```bash
python3 /home/ares/yysnotes/x2md-skill/scripts/convert_x2md.py \
  /path/to/input \
  --output-dir /path/to/out \
  --recursive
```

## Output layout

- `OUTPUT/pdf/**/*.pdf`
- `OUTPUT/md/**/*.md`

## Notes

- For legacy `.ppt`, the script first converts to `.pptx` (temp file) so Markdown can be extracted.
- If a slide deck cannot be parsed to Markdown, PDF conversion still proceeds.
- For `.pdf`, this skill only extracts embedded text. Scanned/image PDFs are skipped (OCR not included).
