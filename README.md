# PDF Processing Scripts

A collection of Python scripts for processing and splitting large PDF documents, specifically designed for the AI Engineering Guidebook.

## Prerequisites

- Python 3.12 or higher
- Required Python packages:
  ```bash
  pip install PyPDF2 PyMuPDF
  ```

## Scripts

### 1. Split PDF by Page Count (`split_pdf.py`)

Splits a large PDF into smaller chunks based on a specified number of pages per file.

**Usage:**
```bash
python split_pdf.py
```

**Configuration:**
- Edit the script to change `pages_per_split` parameter (default: 50 pages)
- Input file: `AI Engineering Guidebook.pdf`
- Output: Creates folder `AI Engineering Guidebook_split` with numbered files

**Example output:**
- `AI Engineering Guidebook_part01_pages1-50.pdf`
- `AI Engineering Guidebook_part02_pages51-100.pdf`
- etc.

### 2. Split PDF by Sections (`extract_toc_and_split.py`)

Reads the table of contents and splits the PDF into separate files for each major section.

**Usage:**
```bash
python extract_toc_and_split.py
```

**Features:**
- Automatically extracts section names from TOC (pages 4-6)
- Creates intelligently named files based on section titles
- Output folder: `AI Engineering Guidebook_by_sections`

**Example output:**
- `01_LLMs.pdf`
- `02_Prompt Engineering.pdf`
- `03_Fine-tuning.pdf`
- `04_RAG.pdf`
- etc.

### 3. Create Executive Summary (`create_executive_summary.py`)

Generates an executive summary by extracting only high-level concepts and definitions, removing detailed examples and code.

**Usage:**
```bash
python create_executive_summary.py
```

**Features:**
- Achieves ~70-80% page reduction
- Keeps: Definitions, concepts, comparisons, architecture overviews
- Removes: Code examples, detailed implementations, sub-bullets, hands-on tutorials
- Automatically selects pages based on TOC analysis
- Output: `AI Engineering Guidebook_Summary.pdf`

**Customization:**
Edit the `analyze_toc_for_executive_summary()` function to:
- Change which topics to include/exclude (modify `True`/`False` flags)
- Adjust page ranges for each topic (modify start_page and end_page)

## Notes

- All scripts expect `AI Engineering Guidebook.pdf` in the same directory
- PDF files are excluded from git (see `.gitignore`)
- Page numbers in scripts are adjusted to account for TOC offset (+1 from TOC page numbers)
