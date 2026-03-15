# Supported Document Types

## Overview

PaddleOCR Document Parsing skill supports a wide variety of document types with optimized extraction strategies for each.

## Financial Documents

### Invoices
- **Supported formats**: PDF, JPG, PNG
- **Key fields**: Invoice number, date, amount, tax rate, seller, buyer
- **Best practices**: Ensure the entire invoice is visible, including stamps/seals

### Receipts
- **Supported formats**: JPG, PNG (mobile photos)
- **Key fields**: Merchant, date, items, total amount
- **Best practices**: Take photo in good lighting, avoid glare

### Bank Statements
- **Supported formats**: PDF
- **Key fields**: Transaction date, description, amount, balance
- **Best practices**: Use original PDFs rather than scans when possible

## Identity Documents

### Business Licenses
- **Supported formats**: PDF, JPG, PNG
- **Key fields**: Company name, registration number, address, legal representative

### ID Cards
- **Supported formats**: JPG, PNG
- **Key fields**: Name, ID number, address, validity period
- **Note**: Ensure both sides are processed separately

## Contracts and Agreements

### Standard Contracts
- **Supported formats**: PDF
- **Key fields**: Parties, terms, dates, signatures
- **Best practices**: Process multi-page contracts as single PDF

## Forms and Applications

### Structured Forms
- **Supported formats**: PDF, scanned images
- **Key fields**: Field labels and corresponding values
- **Best practices**: Use high-resolution scans for best accuracy

## Technical Documents

### Manuals and Specifications
- **Supported formats**: PDF
- **Key fields**: Part numbers, specifications, diagrams
- **Special handling**: Formula recognition for mathematical content

### Research Papers
- **Supported formats**: PDF
- **Key fields**: Title, authors, abstract, sections
- **Special handling**: Table and formula extraction

## Handwritten Documents

### Notes and Letters
- **Supported formats**: JPG, PNG
- **Accuracy**: Lower than printed text (85-90% vs 95%+)
- **Best practices**: Clear handwriting, consistent ink color

## Optimization Tips

### Image Quality
1. **Resolution**: Minimum 200 DPI, 300 DPI recommended
2. **Lighting**: Even, natural lighting without shadows
3. **Contrast**: High contrast between text and background
4. **Orientation**: Keep document flat and properly aligned

### PDF Optimization
1. **Text-based PDFs**: Direct extraction when available
2. **Scanned PDFs**: OCR processing with layout preservation
3. **Multi-page**: Process as single document for context

### Language Settings
- Default: Auto-detect
- Specify language for better accuracy with mixed-language documents
- Supported: 110+ languages

## Common Issues and Solutions

### Low Accuracy
- Check image resolution
- Ensure proper lighting
- Verify language settings
- Consider document preprocessing (deskew, denoise)

### Table Extraction Errors
- Ensure tables have clear borders
- Avoid merged cells when possible
- Check for consistent column alignment

### Missing Fields
- Verify document is fully captured
- Check for overlays or watermarks
- Ensure text is not too small

## Use Cases

### Invoice Processing Automation
Extract invoice data for:
- Expense tracking
- Accounting systems
- Tax reporting
- Audit trails

### Document Digitization
Convert paper documents to:
- Searchable PDFs
- Structured databases
- Knowledge bases
- Archive systems

### Data Entry Automation
Reduce manual entry for:
- Form processing
- Survey responses
- Application forms
- Registration documents

### Content Analysis
Extract and analyze:
- Contract terms
- Research paper content
- Technical specifications
- Legal documents
