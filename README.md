# PDF Combiner with Automatic Bookmarks

A fast, simple utility to combine multiple PDF files into a single document with automatic bookmark generation. Works via a clean CLI or a friendly GUI.

## Features

- **One-command CLI**: `python3 pdf_combiner_cli.py <folder>`
- **Recursive search (optional)**: Finds PDFs in subfolders and prompts you to include them
- **Automatic bookmarks**: Adds a bookmark for each input PDF
- **Natural sorting**: `1.pdf, 2.pdf, 10.pdf` are ordered as humans expect
- **GUI included**: Scan, review, and combine visually

## Quick Start

### Install
```bash
cd combine-pdfs-bookmarks
./install.sh
```

### CLI: simplest usage
```bash
python3 pdf_combiner_cli.py /path/to/folder
```
- Prompts whether to include subfolders
- Shows a summary and asks to confirm
- Saves `combined_pdfs.pdf` in the same folder by default

### CLI: non-interactive
```bash
python3 pdf_combiner_cli.py /path/to/folder -o MyBundle.pdf -r
```
- `-o` sets the output filename
- `-r` includes PDFs from subfolders

### GUI
```bash
python3 pdf_combiner.py
```
- Click “Browse” to select a folder
- Click “Scan for PDFs,” then “Combine PDFs”

## CLI Options
```text
usage: pdf_combiner_cli.py [folder] [-f FOLDER] [-o OUTPUT] [-r] [-y] [--version]

positional arguments:
  folder                Path to folder containing PDF files

optional arguments:
  -f, --folder FOLDER   Path to folder (backward-compatible flag)
  -o, --output OUTPUT   Output filename (adds .pdf if missing)
  -r, --recursive       Include PDFs from subfolders (non-interactive)
  -y, --yes             Assume yes to prompts (non-interactive)
  --version             Show version
```
Notes:
- If you supply both a folder and `-o`, the run is non-interactive.
- Without `-o`, you’ll be prompted and shown a file list; subfolders can be included interactively.

## Examples
- Interactive with prompt for subfolders:
```bash
python3 pdf_combiner_cli.py ~/Docs/Reports
```
- Non-interactive recursive combine with custom name:
```bash
python3 pdf_combiner_cli.py ~/Docs/Reports -o 2024-Annual.pdf -r
```

## Installation Details
- Requires Python 3.7+
- Dependencies in `requirements.txt`:
  - `PyPDF2`
  - `reportlab` (only for the optional `test_demo.py` sample generator)

Install manually if preferred:
```bash
pip3 install -r requirements.txt
```

## Testing with Sample PDFs
Create a sample set in `test_pdfs/`:
```bash
python3 test_demo.py
```
Then try:
```bash
python3 pdf_combiner_cli.py test_pdfs
```

## Troubleshooting
- PyPDF2 not found:
  ```bash
  pip3 install PyPDF2
  ```
- Permission denied for installer:
  ```bash
  chmod +x install.sh && ./install.sh
  ```
- No PDFs found: Confirm extensions are `.pdf` (case-insensitive search is supported).

## License
This utility is provided as-is for personal and educational use.