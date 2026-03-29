# pdfmerge

A command-line tool to merge PDF files from a directory.

## Features

- **Sort**: Alphabetically ascending (`-sA`) or descending (`-sD`)
- **Filter**: Glob pattern matching (`-p "Lecture*.pdf"`)
- **Exclude**: Skip files matching patterns (`-x "*Notes.pdf"`)
- **Recursive**: Include subdirectories (`-r`) or per-folder pattern (`-rf`)
- **Preview**: Dry-run mode to see what would be merged
- **Portable**: Single ~10MB executable, no Python required

## Quick Start

### Build

```bash
cd ~/Scripts/pdfmerge
./build.sh
```

### Install

```bash
mkdir -p ~/.local/bin && cp dist/pdfmerge ~/.local/bin/
```

### Add to fish shell

Add this to `~/.config/fish/config.fish`:

```fish
function pdfmerge
    exec ~/.local/bin/pdfmerge $argv
end
```

Then restart fish or run `source ~/.config/fish/config.fish`.

### Usage

```bash
# Merge all PDFs in current directory
pdfmerge

# Merge lecture PDFs in order
pdfmerge -d ./lectures -sA -p "Lecture*.pdf" -o all_lectures -v

# Exclude files with "Notes" in the name
pdfmerge -sA -p "Lecture*.pdf" -x "*Notes*" -o main_only

# Multiple exclude patterns
pdfmerge -x "*Notes.pdf" -x "draft*.pdf" -x "*old*"

# Preview without merging
pdfmerge -r --dry-run -v

# Recursive with pattern per folder
pdfmerge -rf -p "*Notes.pdf" -o notes_only
```

### Options

| Option | Description |
|--------|-------------|
| `-d, --directory` | Source directory (default: current) |
| `-o, --output` | Output filename (.pdf optional) |
| `-sA` | Sort ascending (A→Z) |
| `-sD` | Sort descending (Z→A) |
| `-p, --pattern` | Glob pattern filter |
| `-x, --exclude` | Exclude pattern (can be used multiple times) |
| `-r, --recursive` | Include subdirectories |
| `-rf` | Recursive + pattern per folder |
| `-v, --verbose` | Show files being merged |
| `--dry-run` | Preview without creating file |
| `-h, --help` | Show help |

## License

MIT
