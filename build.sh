#!/bin/bash
# Build standalone pdfmerge executable using PyInstaller

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

echo "Installing dependencies..."
.venv/bin/pip install -q pyinstaller pypdf

echo "Building pdfmerge executable..."
.venv/bin/pyinstaller --clean pdfmerge.spec

echo ""
echo "✓ Build complete! Executable location:"
echo "  $SCRIPT_DIR/dist/pdfmerge"
echo ""
echo "To install:"
echo "  # User-only (recommended):"
echo "  mkdir -p ~/.local/bin && cp dist/pdfmerge ~/.local/bin/"
echo ""
echo "  # System-wide (requires sudo):"
echo "  sudo cp dist/pdfmerge /usr/local/bin/"
echo ""
echo "To add fish shell completions:"
echo "  cat $SCRIPT_DIR/pdfmerge.fish >> ~/.config/fish/config.fish"
