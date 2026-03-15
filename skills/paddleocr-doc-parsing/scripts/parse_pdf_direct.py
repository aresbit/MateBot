#!/usr/bin/env python3
"""
PaddleOCR PDF Parser - Direct PDF support
Based on official API documentation
"""

import os
import sys
import argparse
import base64
import json
import requests
import time
from pathlib import Path


def get_api_credentials():
    """Get API credentials from environment variables."""
    api_url = os.environ.get("PADDLEOCR_API_URL")
    access_token = os.environ.get("PADDLEOCR_ACCESS_TOKEN")

    if not api_url or not access_token:
        print("Error: PADDLEOCR_API_URL and PADDLEOCR_ACCESS_TOKEN must be set", file=sys.stderr)
        sys.exit(1)

    return api_url, access_token


def call_api_with_retry(api_url, payload, headers, max_retries=3, delay=3):
    """Call API with retry logic for handling transient errors."""
    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=300)

            if response.status_code == 200:
                return response.json()

            print(f"Attempt {attempt + 1}/{max_retries}: API returned {response.status_code}", file=sys.stderr)

            if attempt < max_retries - 1:
                print(f"Waiting {delay}s before retry...", file=sys.stderr)
                time.sleep(delay)
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Request failed - {e}", file=sys.stderr)
            if attempt < max_retries - 1:
                print(f"Waiting {delay}s before retry...", file=sys.stderr)
                time.sleep(delay)
            else:
                raise

    return None


def parse_pdf(file_path: str, api_url: str, access_token: str, output_dir: str = None) -> dict:
    """Parse a PDF using PaddleOCR API."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Default output dir: same directory as input file, named {filename}_ocr
    if output_dir is None:
        output_dir = file_path.parent / f"{file_path.stem}_ocr"
    else:
        output_dir = Path(output_dir)

    # Read and encode file
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        file_data = base64.b64encode(file_bytes).decode("ascii")

    # Prepare headers
    headers = {
        "Authorization": f"token {access_token}",
        "Content-Type": "application/json"
    }

    # Prepare payload
    # fileType: 0 for PDF, 1 for images
    suffix = file_path.suffix.lower()
    file_type = 0 if suffix == ".pdf" else 1

    payload = {
        "file": file_data,
        "fileType": file_type,
        "useDocOrientationClassify": False,
        "useDocUnwarping": False,
        "useChartRecognition": False,
    }

    # Send request with retry
    print(f"Sending {file_path} to PaddleOCR API...", file=sys.stderr)
    result = call_api_with_retry(api_url, payload, headers)

    if result is None:
        raise RuntimeError("API call failed after all retries")

    # Save results
    os.makedirs(output_dir, exist_ok=True)

    all_markdown = []
    layout_results = result.get("result", {}).get("layoutParsingResults", [])

    for i, res in enumerate(layout_results):
        md_content = res.get("markdown", {}).get("text", "")
        all_markdown.append(f"\n## Page {i + 1}\n\n{md_content}")

        md_filename = output_dir / f"page_{i + 1}.md"
        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Page {i + 1} saved to: {md_filename}", file=sys.stderr)

        # Download images if any
        images = res.get("markdown", {}).get("images", {})
        for img_path, img_url in images.items():
            # Clean img_path to prevent directory traversal
            img_name = Path(img_path).name
            full_img_path = output_dir / img_name
            try:
                img_bytes = requests.get(img_url, timeout=60).content
                with open(full_img_path, "wb") as img_file:
                    img_file.write(img_bytes)
                print(f"Image saved: {full_img_path}", file=sys.stderr)
            except Exception as e:
                print(f"Failed to download image {img_name}: {e}", file=sys.stderr)

    return {
        "raw_result": result,
        "markdown": "".join(all_markdown),
        "total_pages": len(layout_results),
        "output_dir": str(output_dir)
    }


def main():
    parser = argparse.ArgumentParser(description="Parse PDF/image using PaddleOCR")
    parser.add_argument("file", help="Path to the PDF or image file")
    parser.add_argument("--output", "-o", help="Output directory (default: {filename}_ocr in same directory)", default=None)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--retries", type=int, default=3, help="Number of retries on API failure (default: 3)")

    args = parser.parse_args()

    # Get credentials
    api_url, access_token = get_api_credentials()

    try:
        # Parse PDF
        result = parse_pdf(args.file, api_url, access_token, args.output)

        # Output to stdout
        if args.format == "markdown":
            print(result["markdown"])
        else:
            print(json.dumps(result["raw_result"], ensure_ascii=False, indent=2))

        print(f"\n---", file=sys.stderr)
        print(f"Total pages: {result['total_pages']}", file=sys.stderr)
        print(f"Output directory: {result['output_dir']}", file=sys.stderr)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
