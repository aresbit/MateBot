#!/usr/bin/env python3
"""
Extract specific fields from documents using PaddleOCR
Supports common document types: invoices, receipts, forms, etc.
"""

import os
import sys
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

# Import the parse function from parse_document
sys.path.insert(0, str(Path(__file__).parent))
from parse_document import parse_document, get_api_credentials


INVOICE_PATTERNS = {
    "invoice_number": [
        r"发票号码[:：]?\s*(\d+)",
        r"发票代码[:：]?\s*(\d+)",
        r"No[:：]?\s*(\d+)"
    ],
    "date": [
        r"日期[:：]?\s*(\d{4}[年/-]\d{1,2}[月/-]\d{1,2}[日]?)",
        r"开票日期[:：]?\s*(\d{4}[年/-]\d{1,2}[月/-]\d{1,2}[日]?)"
    ],
    "amount": [
        r"金额[:：]?\s*[¥￥]?\s*(\d+[\.,]?\d*)",
        r"价税合计[:：]?\s*[¥￥]?\s*(\d+[\.,]?\d*)",
        r"合计金额[:：]?\s*[¥￥]?\s*(\d+[\.,]?\d*)"
    ],
    "tax_rate": [
        r"税率[:：]?\s*(\d+%)",
        r"税点[:：]?\s*(\d+%)"
    ],
    "seller": [
        r"销售方[:：]?\s*([^\n]+)",
        r"卖方[:：]?\s*([^\n]+)"
    ],
    "buyer": [
        r"购买方[:：]?\s*([^\n]+)",
        r"买方[:：]?\s*([^\n]+)",
        r"购方[:：]?\s*([^\n]+)"
    ]
}

RECEIPT_PATTERNS = {
    "merchant": [
        r"商户[:：]?\s*([^\n]+)",
        r"商家[:：]?\s*([^\n]+)",
        r"店名[:：]?\s*([^\n]+)"
    ],
    "date": [
        r"日期[:：]?\s*(\d{4}[年/-]\d{1,2}[月/-]\d{1,2}[日]?)",
        r"时间[:：]?\s*(\d{4}[年/-]\d{1,2}[月/-]\d{1,2}[日]?)"
    ],
    "total": [
        r"总计[:：]?\s*[¥￥]?\s*(\d+[\.,]?\d*)",
        r"合计[:：]?\s*[¥￥]?\s*(\d+[\.,]?\d*)",
        r"实付[:：]?\s*[¥￥]?\s*(\d+[\.,]?\d*)"
    ]
}


def extract_with_patterns(text: str, patterns: Dict[str, List[str]]) -> Dict[str, Optional[str]]:
    """Extract fields using regex patterns."""
    results = {}

    for field, pattern_list in patterns.items():
        value = None
        for pattern in pattern_list:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).strip() if match.groups() else match.group(0).strip()
                break
        results[field] = value

    return results


def extract_invoice_fields(text: str) -> Dict[str, Optional[str]]:
    """Extract fields from invoice text."""
    return extract_with_patterns(text, INVOICE_PATTERNS)


def extract_receipt_fields(text: str) -> Dict[str, Optional[str]]:
    """Extract fields from receipt text."""
    return extract_with_patterns(text, RECEIPT_PATTERNS)


def extract_custom_fields(text: str, fields_config: Dict[str, List[str]]) -> Dict[str, Optional[str]]:
    """Extract custom fields based on user-defined patterns."""
    return extract_with_patterns(text, fields_config)


def main():
    parser = argparse.ArgumentParser(description="Extract fields from documents")
    parser.add_argument("file", help="Path to the document file")
    parser.add_argument("--type", choices=["invoice", "receipt", "auto", "custom"],
                        default="auto", help="Document type")
    parser.add_argument("--fields", help="Custom fields to extract (JSON format)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--format", choices=["json", "text"],
                        default="json", help="Output format")

    args = parser.parse_args()

    # Get credentials
    api_url, access_token = get_api_credentials()

    try:
        # Parse document
        result = parse_document(args.file, api_url, access_token)

        # Get text content
        text = result.get("text", "")
        if "markdown" in result:
            text = result["markdown"]

        # Determine document type and extract fields
        doc_type = args.type
        if doc_type == "auto":
            # Auto-detect based on keywords
            if "发票" in text or "invoice" in text.lower():
                doc_type = "invoice"
            elif "收据" in text or "receipt" in text.lower() or "小票" in text:
                doc_type = "receipt"
            else:
                doc_type = "generic"

        # Extract fields based on type
        if doc_type == "invoice":
            extracted = extract_invoice_fields(text)
        elif doc_type == "receipt":
            extracted = extract_receipt_fields(text)
        elif doc_type == "custom" and args.fields:
            custom_fields = json.loads(args.fields)
            extracted = extract_custom_fields(text, custom_fields)
        else:
            # Generic extraction - return all text
            extracted = {"text": text}

        # Add metadata
        output = {
            "document_type": doc_type,
            "file": args.file,
            "extracted_fields": extracted
        }

        # Format and output
        if args.format == "json":
            output_str = json.dumps(output, ensure_ascii=False, indent=2)
        else:
            lines = [f"Document Type: {doc_type}", f"File: {args.file}", ""]
            for field, value in extracted.items():
                lines.append(f"{field}: {value}")
            output_str = "\n".join(lines)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_str)
            print(f"Output written to: {args.output}")
        else:
            print(output_str)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
