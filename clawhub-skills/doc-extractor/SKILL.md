---
name: Document Text Extractor
version: 1.0.0
description: Extract readable text from DOCX, PDF, and plain-text files using Python stdlib (zipfile + xml.etree) with optional pymupdf for PDF support. No paid APIs, no OCR cloud services.
tags: ocr,documents,pdf,text-extraction,python,docx,cli
---

# Document Text Extractor

A zero-overhead CLI tool that extracts readable text from common document formats — DOCX (Microsoft Word), PDF (when pymupdf is available), and plain text files — using Python's standard library wherever possible. No cloud APIs, no subscription fees, no heavyweight installs.

Built for document processing pipelines, AI training data preparation, search indexing, and batch text extraction workflows.

## Install

```bash
# Basic install (DOCX + TXT support via stdlib)
cp doc_extractor.py /usr/local/bin/doc-extractor
chmod +x /usr/local/bin/doc-extractor

# Optional: add PDF support
pip install pymupdf

# Or run directly
python doc_extractor.py --help
```

## Commands

| Command | Description |
|---------|-------------|
| `extract <file>` | Extract text from a single file (DOCX, PDF, TXT) |
| `extract <file> --output out.txt` | Save extracted text to a file |
| `list-formats` | Show supported file formats and requirements |
| `batch <dir>` | Extract text from all supported files in a directory |
| `batch <dir> --outdir ./texts` | Save all extracts to a specific output directory |
| `batch <dir> --ext .docx,.txt` | Only process files with specific extensions |

## Usage

```bash
# Extract text from a Word document
python doc_extractor.py extract report.docx

# Extract text from a PDF (requires pymupdf)
python doc_extractor.py extract paper.pdf

# Save to file
python doc_extractor.py extract notes.docx --output cleaned.txt

# Batch extract all documents in a folder
python doc_extractor.py batch ./documents/

# Batch extract to a separate output folder
python doc_extractor.py batch ./invoices/ --outdir ./extracted/

# Only process specific file types
python doc_extractor.py batch ./reports/ --ext .docx,.pdf

# List supported formats
python doc_extractor.py list-formats
```

## Features

- **Zero dependencies for DOCX** — uses `zipfile` + `xml.etree.ElementTree` from Python stdlib to parse Office Open XML
- **Optional PDF support** — when `pymupdf` is installed, extracts text from PDFs with layout preservation
- **Plain text fallback** — reads `.txt` files directly (with encoding auto-detection)
- **Batch processing** — recursively walks directories and extracts every supported file
- **Encoding detection** — handles UTF-8, Latin-1, and UTF-16 text files
- **Progress reporting** — shows file count and status during batch operations
- **Error resilient** — skips corrupt files with clear error messages instead of crashing
- **No cloud** — everything runs locally, no data leaves your machine

## Examples

```bash
# Extract a Word document for indexing
python doc_extractor.py extract dissertation.docx --output dissertation.txt

# Batch process a research paper folder
python doc_extractor.py batch ~/papers/ --outdir ~/papers-text/

# Extract text from a mix of formats
python doc_extractor.py extract report.docx
python doc_extractor.py extract invoice.pdf
python doc_extractor.py extract readme.txt

# Prepare documents for LLM context
python doc_extractor.py batch ./knowledge-base/ --outdir ./kb-text/
```

## Format Support

| Format | Support | Dependency |
|--------|---------|------------|
| `.docx` | Full | stdlib only (`zipfile` + `xml.etree`) |
| `.docx` (tables) | Full | stdlib only |
| `.pdf` | Full | `pymupdf` (pip install) |
| `.txt` | Full | stdlib only |
| `.md` | Full (read as plain text) | stdlib only |
| `.csv` | Full (read as plain text) | stdlib only |
| `.json` | Full (read as plain text) | stdlib only |
| `.xml` | Direct (read as plain text) | stdlib only |
| `.html` | Direct (read as plain text) | stdlib only |

## Why Document Text Extractor?

Most document extraction tools fall into two camps: cloud APIs that require sending your data to a third party (Google Cloud Vision, Azure Form Recognizer, AWS Textract), or heavyweight local installs (Tesseract, Poppler, LibreOffice headless). This tool occupies the sweet spot — **it handles the most common format (DOCX) with zero dependencies**, adds PDF support with a single `pip install`, and works entirely offline.

Perfect for:
- **AI/LLM pipelines** — prepare training data from Word documents
- **Search indexing** — extract text for Elasticsearch, Meilisearch, or Whoosh
- **Document archival** — convert office documents to plain text for long-term storage
- **CI/CD pipelines** — validate document content in automated workflows
- **Privacy-conscious environments** — no data ever leaves your network

## Support

- File an issue on the [ClawHub registry](https://clawhub.nousresearch.com)
- MIT License — free to use, modify, and share
- Contributions welcome — add support for ODP, ODS, RTF, and more formats
