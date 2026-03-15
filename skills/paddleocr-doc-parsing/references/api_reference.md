# PaddleOCR API Reference

## Overview

PaddleOCR is Baidu's open-source OCR system that provides state-of-the-art text detection and recognition capabilities.

## API Endpoints

### Document Parsing

**Endpoint**: `POST /api/v1/ocr/document`

**Headers**:
- `Authorization`: Bearer YOUR_ACCESS_TOKEN
- `Content-Type`: application/json

**Request Body**:
```json
{
  "file": "base64_encoded_file_content",
  "file_type": "pdf|jpg|png|bmp|tiff",
  "options": {
    "layout_analysis": true,
    "table_recognition": true,
    "formula_recognition": true,
    "language": "auto"
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "text": "Extracted text content",
    "markdown": "Markdown formatted content",
    "layout": [
      {
        "type": "text|table|title|heading|formula",
        "content": "...",
        "bbox": [x1, y1, x2, y2]
      }
    ],
    "tables": [...],
    "pages": [
      {
        "page_num": 1,
        "text": "...",
        "blocks": [...]
      }
    ]
  }
}
```

## Supported File Formats

| Format | Extension | Max Size |
|--------|-----------|----------|
| PDF | .pdf | 50MB |
| JPEG | .jpg, .jpeg | 10MB |
| PNG | .png | 10MB |
| BMP | .bmp | 10MB |
| TIFF | .tiff, .tif | 20MB |

## Language Support

PaddleOCR supports 110+ languages including:
- Chinese (Simplified & Traditional)
- English
- Japanese
- Korean
- French
- German
- Spanish
- Portuguese
- Arabic
- Russian
- And many more...

## Features

### Layout Analysis
Detects and categorizes document elements:
- Text blocks
- Tables
- Titles and headings
- Formulas
- Images
- Headers/footers

### Table Recognition
Extracts tables and converts them to structured formats:
- Preserves cell relationships
- Supports merged cells
- Exports as Markdown tables

### Formula Recognition
Detects and extracts mathematical formulas using LaTeX format.

## Rate Limits

- Free tier: 10,000 pages/day
- Standard tier: 100,000 pages/day
- Enterprise: Custom limits

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid token |
| 403 | Forbidden - Rate limit exceeded |
| 413 | Payload Too Large - File exceeds size limit |
| 500 | Internal Server Error |

## Best Practices

1. **Pre-processing**: For best results, ensure documents are:
   - Well-lit and clear
   - Properly oriented (not rotated)
   - High enough resolution (300 DPI recommended for scans)

2. **Batch Processing**: For large documents:
   - Split into smaller chunks
   - Use asynchronous API for files > 10MB

3. **Error Handling**: Always implement retry logic with exponential backoff

## SDK and Tools

Official SDKs available for:
- Python
- Java
- JavaScript/Node.js
- Go

## Resources

- Official Website: https://paddleocr.com
- GitHub: https://github.com/PaddlePaddle/PaddleOCR
- Documentation: https://paddleocr.github.io/PaddleOCR/
