# Quick Start Guide

## 🚀 Get Started Fast

### 1) Install
```bash
./install.sh
```

### 2) Run from Terminal (CLI)
```bash
python3 pdf_combiner_cli.py /path/to/folder
```
- Prompts to include subfolders
- Confirms file list and output name

Non-interactive example:
```bash
python3 pdf_combiner_cli.py /path/to/folder -o MyBundle.pdf -r
```

### 3) Or Use the GUI
```bash
python3 pdf_combiner.py
```
- Browse to your folder → Scan for PDFs → Combine PDFs

## 🔧 Troubleshooting

- "PyPDF2 not found"?
```bash
pip3 install PyPDF2
```

- Permission denied?
```bash
chmod +x install.sh && ./install.sh
```

You're ready to combine PDFs with automatic bookmarks! 📚✨