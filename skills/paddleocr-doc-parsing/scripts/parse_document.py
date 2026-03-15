#!/usr/bin/env python3
"""
PaddleOCR Document Parser
Parse documents (PDF, images) using PaddleOCR API
"""

import os
import sys
import argparse
import base64
import json
import requests
from pathlib import Path
from typing import Optional


def get_api_credentials():
    """Get API credentials from environment variables."""
    api_url = os.environ.get("PADDLEOCR_API_URL")
    access_token = os.environ.get("PADDLEOCR_ACCESS_TOKEN")

    if not api_url or not access_token:
        print("Error: PADDLEOCR_API_URL and PADDLEOCR_ACCESS_TOKEN must be set", file=sys.stderr)
        sys.exit(1)

    return api_url, access_token


def encode_file(file_path: str) -> str:
    """Encode file to base64."""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def parse_document(file_path: str, api_url: str, access_token: str) -> dict:
    """Parse a document using PaddleOCR API."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine file type
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        file_type = "pdf"
    elif suffix in [".jpg", ".jpeg"]:
        file_type = "jpg"
    elif suffix == ".png":
        file_type = "png"
    elif suffix == ".bmp":
        file_type = "bmp"
    elif suffix == ".tiff":
        file_type = "tiff"
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    # Encode file
    file_content = encode_file(str(file_path))

    # Prepare request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "file": f"data:image/{file_type};base64,{file_content}",
        "file_type": file_type,
        "options": {
            "layout_analysis": True,
            "table_recognition": True,
            "formula_recognition": True
        }
    }

    # Send request
    response = requests.post(api_url, headers=headers, json=payload, timeout=300)
    response.raise_for_status()

    return response.json()


def format_output(result: dict, output_format: str = "markdown") -> str:
    """Format the parsing result."""
    if output_format == "markdown":
        # Convert result to markdown
        md_parts = []

        if "layout" in result:
            for block in result["layout"]:
                block_type = block.get("type", "text")
                content = block.get("content", "")

                if block_type == "title":
                    md_parts.append(f"# {content}\n")
                elif block_type == "heading":
                    md_parts.append(f"## {content}\n")
                elif block_type == "table":
                    md_parts.append(f"\n{content}\n")
                elif block_type == "formula":
                    md_parts.append(f"$${content}$$\n")
                else:
                    md_parts.append(f"{content}\n")

        if "text" in result:
            md_parts.append(result["text"])

        return "\n".join(md_parts)

    elif output_format == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)

    else:
        return str(result)


def main():
    parser = argparse.ArgumentParser(description="Parse documents using PaddleOCR")
    parser.add_argument("file", help="Path to the document file")
    parser.add_argument("--format", choices=["markdown", "json", "raw"],
                        default="markdown", help="Output format")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    # Get credentials
    api_url, access_token = get_api_credentials()

    try:
        # Parse document
        result = parse_document(args.file, api_url, access_token)

        # Format output
        output = format_output(result, args.format)

        # Write output
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Output written to: {args.output}")
        else:
            print(output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
