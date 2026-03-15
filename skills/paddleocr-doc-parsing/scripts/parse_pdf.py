#!/usr/bin/env python3
"""
PaddleOCR PDF Parser
Converts PDF to images and parses using PaddleOCR API
"""

import os
import sys
import argparse
import base64
import json
import requests
from pathlib import Path
from pdf2image import convert_from_path
import tempfile


def get_api_credentials():
    """Get API credentials from environment variables."""
    api_url = os.environ.get("PADDLEOCR_API_URL")
    access_token = os.environ.get("PADDLEOCR_ACCESS_TOKEN")

    if not api_url or not access_token:
        print("Error: PADDLEOCR_API_URL and PADDLEOCR_ACCESS_TOKEN must be set", file=sys.stderr)
        sys.exit(1)

    return api_url, access_token


def encode_image(image_path: str) -> str:
    """Encode image to base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def parse_image(image_path: str, api_url: str, access_token: str) -> dict:
    """Parse an image using PaddleOCR API."""
    # Encode image
    file_content = encode_image(image_path)

    # Prepare request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "file": f"data:image/png;base64,{file_content}",
        "file_type": "png",
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


def parse_pdf(pdf_path: str, api_url: str, access_token: str, dpi: int = 200) -> dict:
    """Parse a PDF by converting to images first."""
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")

    # Convert PDF to images
    print(f"Converting PDF to images (DPI={dpi})...", file=sys.stderr)
    images = convert_from_path(str(pdf_path), dpi=dpi)

    all_results = {
        "pages": [],
        "total_pages": len(images)
    }

    # Create temp directory for images
    with tempfile.TemporaryDirectory() as temp_dir:
        for i, image in enumerate(images, 1):
            print(f"Processing page {i}/{len(images)}...", file=sys.stderr)

            # Save image to temp file
            image_path = Path(temp_dir) / f"page_{i}.png"
            image.save(str(image_path), "PNG")

            # Parse image
            result = parse_image(str(image_path), api_url, access_token)
            all_results["pages"].append({
                "page_num": i,
                "result": result
            })

    return all_results


def format_output(result: dict, output_format: str = "markdown") -> str:
    """Format the parsing result."""
    if output_format == "markdown":
        md_parts = []

        for page in result.get("pages", []):
            page_num = page.get("page_num", 0)
            page_result = page.get("result", {})

            md_parts.append(f"\n## Page {page_num}\n")

            # Handle different response structures
            data = page_result.get("data", page_result)

            if "markdown" in data:
                md_parts.append(data["markdown"])
            elif "text" in data:
                md_parts.append(data["text"])
            elif "layout" in data:
                for block in data["layout"]:
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

        return "\n".join(md_parts)

    elif output_format == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)

    else:
        return str(result)


def main():
    parser = argparse.ArgumentParser(description="Parse PDF using PaddleOCR")
    parser.add_argument("file", help="Path to the PDF file")
    parser.add_argument("--format", choices=["markdown", "json", "raw"],
                        default="markdown", help="Output format")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--dpi", type=int, default=200, help="DPI for PDF to image conversion (default: 200)")

    args = parser.parse_args()

    # Get credentials
    api_url, access_token = get_api_credentials()

    try:
        # Parse PDF
        result = parse_pdf(args.file, api_url, access_token, dpi=args.dpi)

        # Format output
        output = format_output(result, args.format)

        # Write output
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Output written to: {args.output}", file=sys.stderr)
        else:
            print(output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
