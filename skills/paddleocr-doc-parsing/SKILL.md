---
name: paddleocr-doc-parsing
description: Document parsing and OCR using PaddleOCR. Extract text, tables, and structured data from PDFs and images (JPG, PNG, BMP, TIFF). Supports 110+ languages and outputs Markdown format preserving document layout. Use when processing documents for data extraction, invoice parsing, form recognition, or converting scanned documents to structured text. Requires PADDLEOCR_API_URL and PADDLEOCR_ACCESS_TOKEN environment variables.
---

# PaddleOCR Document Parsing

This skill integrates Baidu's PaddleOCR to provide powerful document parsing capabilities for Claude Code.

## Features

- **Multi-format support**: PDF, JPG, PNG, BMP, TIFF
- **Layout analysis**: Automatically detects text, tables, formulas, headers, and other document elements
- **Multi-language OCR**: Covers 110+ languages including Chinese, English, Japanese, Korean
- **Structured output**: Returns Markdown format that preserves document hierarchy
- **Direct PDF support**: No conversion needed, PDFs parsed directly via API

## Setup

### 1. Get API Credentials

Visit [PaddleOCR](https://paddleocr.com) to get API credentials:

1. Register and verify your phone number
2. Select "PaddleOCR-VL-1.5" model
3. Copy TOKEN and API_URL from the example code
4. Free daily quota: tens of thousands of pages

### 2. Configure Environment Variables

Add to `~/.zshrc` or `~/.claude/.env`:

```bash
export PADDLEOCR_API_URL="your_api_url_here"
export PADDLEOCR_ACCESS_TOKEN="your_access_token_here"
```

## Usage

### Parse PDF Document

```bash
python3 scripts/parse_pdf_direct.py /path/to/document.pdf
```

**Output**:
- Markdown printed to stdout
- `{filename}_ocr/` directory created in same folder as PDF
- Each page saved as separate `.md` file
- Images extracted and saved to output directory

**Options**:
```bash
python3 scripts/parse_pdf_direct.py /path/to/document.pdf --output /custom/output/dir
python3 scripts/parse_pdf_direct.py /path/to/document.pdf --format json
```

### Parse Image

Same script handles images (fileType detected automatically):

```bash
python3 scripts/parse_pdf_direct.py /path/to/invoice.jpg
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/parse_pdf_direct.py` | Main parsing script for PDF and images |
| `scripts/parse_document.py` | Alternative script (legacy API format) |
| `scripts/extract_fields.py` | Field extraction for common document types |

## References

- `references/api_reference.md` - API endpoint specifications
- `references/document_types.md` - Supported documents and best practices

## API Response Format

```json
{
  "result": {
    "layoutParsingResults": [
      {
        "markdown": {
          "text": "## Page content...",
          "images": {"img1.png": "https://..."}
        }
      }
    ]
  }
}
```

## Error Handling

The API may occasionally return 500 errors due to service load. The script includes automatic retry logic. If parsing fails:

1. Wait a few seconds
2. Retry the request
3. Check API credentials are correct
