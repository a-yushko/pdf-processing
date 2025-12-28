import PyPDF2
import re
import os

def extract_toc_from_pages(pdf_path, pages=[3, 4, 5]):  # 0-indexed, so pages 4,5,6
    """Extract text from table of contents pages."""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        toc_text = ""
        for page_num in pages:
            if page_num < len(pdf_reader.pages):
                toc_text += pdf_reader.pages[page_num].extract_text()
    return toc_text

def parse_toc(toc_text):
    """Parse the table of contents to extract sections and page numbers."""
    sections = []
    
    # Define major sections manually based on the TOC structure
    # These appear to be the main chapter-level sections
    major_sections = [
        ("LLMs", 7),
        ("Prompt Engineering", 50),
        ("Fine-tuning", 67),
        ("RAG", 106),
        ("Context Engineering", 147),
        ("AI Agents", 177),
        ("MCP", 265),
        ("LLM Optimization", 305),
        ("LLM Evaluation", 332),
        ("LLM Deployment", 359),
        ("LLM Observability", 371),
    ]
    
    print("=" * 80)
    print("MAJOR SECTIONS IDENTIFIED:")
    print("=" * 80)
    
    for section_name, page_num in major_sections:
        sections.append({
            'name': section_name,
            'start_page': page_num
        })
        print(f"Section: {section_name} -> Page {page_num}")
    
    print("=" * 80)
    
    return sections

def clean_filename(name):
    """Clean section name to make it a valid filename."""
    # Remove invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace dots at the end with nothing (common in TOC)
    name = name.rstrip('.')
    # Replace multiple spaces with single space
    name = re.sub(r'\s+', ' ', name)
    # Limit length
    if len(name) > 100:
        name = name[:100]
    return name.strip()

def split_pdf_by_sections(input_pdf, sections):
    """Split PDF based on sections from TOC."""
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    output_dir = os.path.join(os.path.dirname(input_pdf), f"{base_name}_by_sections")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        print(f"\nTotal pages in PDF: {total_pages}")
        print(f"Creating {len(sections)} section files...\n")
        
        for i, section in enumerate(sections):
            pdf_writer = PyPDF2.PdfWriter()
            
            start_page = section['start_page'] - 1  # Convert to 0-indexed
            
            # Determine end page (start of next section or end of document)
            if i + 1 < len(sections):
                end_page = sections[i + 1]['start_page'] - 1
            else:
                end_page = total_pages
            
            # Add pages to the writer
            for page_num in range(start_page, end_page):
                if page_num < total_pages:
                    pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # Create filename
            clean_name = clean_filename(section['name'])
            output_filename = os.path.join(
                output_dir,
                f"{i+1:02d}_{clean_name}.pdf"
            )
            
            with open(output_filename, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            pages_count = end_page - start_page
            print(f"Created: {os.path.basename(output_filename)} ({pages_count} pages, {start_page+1}-{end_page})")
        
        print(f"\nSplit complete! {len(sections)} files created in: {output_dir}")

if __name__ == "__main__":
    input_file = r"AI Engineering Guidebook.pdf"
    
    print("Step 1: Extracting table of contents from pages 4, 5, 6...\n")
    toc_text = extract_toc_from_pages(input_file, pages=[3, 4, 5])  # 0-indexed
    
    print("\nStep 2: Parsing table of contents...\n")
    sections = parse_toc(toc_text)
    
    if not sections:
        print("\nNo sections found! The TOC format might be different than expected.")
        print("Please review the extracted text above and adjust the parsing logic.")
    else:
        print(f"\nStep 3: Splitting PDF into {len(sections)} sections...\n")
        split_pdf_by_sections(input_file, sections)
