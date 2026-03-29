#!/usr/bin/env python3
"""
pdfmerge - Merge PDF files from a directory.

Usage:
    pdfmerge [options]

Options:
    -d, --directory DIR   Source directory (default: current directory)
    -o, --output FILE     Output filename (.pdf extension optional)
    -sA                   Sort ascending alphabetically (A→Z)
    -sD                   Sort descending alphabetically (Z→A)
    -p, --pattern PAT     Glob pattern to filter files (e.g., "Lecture*.pdf")
    -r, --recursive       Include PDFs from subdirectories
    -rf                   Recursive + apply pattern per folder
    -v, --verbose         Show files being merged
    --dry-run             Preview merge without creating file
    -h, --help            Show this help message
"""

import argparse
import fnmatch
import os
import sys
from pathlib import Path

# PyInstaller bundles these imports
import pypdf
from pypdf import PdfReader, PdfWriter


def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge PDF files from a directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdfmerge -d ./lectures -o combined
  pdfmerge -sA -p "Lecture*.pdf" -v
  pdfmerge -rf -p "*.pdf" -o all_lectures
        """,
    )
    parser.add_argument("-d", "--directory", type=str, default=".",
                        help="Source directory (default: current directory)")
    parser.add_argument("-o", "--output", type=str, default="merged.pdf",
                        help="Output filename (.pdf extension optional, default: merged.pdf)")
    parser.add_argument("-sA", action="store_true",
                        help="Sort ascending alphabetically (A→Z)")
    parser.add_argument("-sD", action="store_true",
                        help="Sort descending alphabetically (Z→A)")
    parser.add_argument("-p", "--pattern", type=str, default="*.pdf",
                        help='Glob pattern to filter files (default: "*.pdf")')
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Include PDFs from subdirectories")
    parser.add_argument("-rf", action="store_true",
                        help="Recursive + apply pattern per folder")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show files being merged")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview merge without creating file")
    return parser.parse_args()


def ensure_pdf_extension(filename: str) -> str:
    """Add .pdf extension if not present."""
    if not filename.lower().endswith(".pdf"):
        return filename + ".pdf"
    return filename


def collect_pdfs(directory: Path, pattern: str, recursive: bool, rf_mode: bool) -> list[Path]:
    """Collect PDF files based on options."""
    pdfs = []

    if rf_mode:
        # Recursive + pattern per folder
        for root, dirs, files in os.walk(directory):
            folder_pdfs = [f for f in files if fnmatch.fnmatch(f, pattern)]
            pdfs.extend(Path(root) / f for f in sorted(folder_pdfs))
    elif recursive:
        # Simple recursive - all matching PDFs
        for root, dirs, files in os.walk(directory):
            for f in files:
                if fnmatch.fnmatch(f, pattern):
                    pdfs.append(Path(root) / f)
    else:
        # Flat directory only
        for f in directory.iterdir():
            if f.is_file() and fnmatch.fnmatch(f.name, pattern):
                pdfs.append(f)

    return pdfs


def sort_pdfs(pdfs: list[Path], ascending: bool, descending: bool) -> list[Path]:
    """Sort PDF list based on options."""
    if ascending and not descending:
        return sorted(pdfs, key=lambda p: p.name.lower())
    elif descending and not ascending:
        return sorted(pdfs, key=lambda p: p.name.lower(), reverse=True)
    return pdfs  # No sorting - filesystem order


def main():
    args = parse_args()

    directory = Path(args.directory).resolve()
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    output_file = Path(ensure_pdf_extension(args.output))
    if not output_file.is_absolute():
        output_file = directory / output_file

    # Collect and sort PDFs
    pdfs = collect_pdfs(directory, args.pattern, args.recursive, args.rf)
    pdfs = sort_pdfs(pdfs, args.sA, args.sD)

    if not pdfs:
        print(f"No PDF files found matching '{args.pattern}' in '{directory}'.", file=sys.stderr)
        sys.exit(1)

    # Verbose output
    if args.verbose:
        print(f"Directory: {directory}")
        print(f"Pattern: {args.pattern}")
        print(f"Output: {output_file}")
        print(f"Files to merge ({len(pdfs)}):")
        for i, pdf in enumerate(pdfs, 1):
            print(f"  {i}. {pdf.name}")
        print()

    # Dry run
    if args.dry_run:
        print("[DRY RUN] Would merge the following files:")
        for pdf in pdfs:
            print(f"  - {pdf}")
        print(f"\n[DRY RUN] Output would be: {output_file}")
        return

    # Merge PDFs
    if args.verbose:
        print(f"Merging {len(pdfs)} PDF(s)...")

    writer = PdfWriter()
    try:
        for pdf in pdfs:
            reader = PdfReader(str(pdf))
            writer.append(reader)
        writer.write(str(output_file))
    except Exception as e:
        print(f"Error merging PDFs: {e}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"Successfully created: {output_file}")
    else:
        print(f"Merged {len(pdfs)} PDF(s) into {output_file.name}")


if __name__ == "__main__":
    main()
