import PyPDF2
import os

def split_pdf(input_pdf, pages_per_split=50):
    """
    Split a large PDF into smaller chunks.
    
    Args:
        input_pdf: Path to the input PDF file
        pages_per_split: Number of pages per output file (default: 50)
    """
    # Get the base name without extension
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    output_dir = os.path.join(os.path.dirname(input_pdf), f"{base_name}_split")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the PDF
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        print(f"Total pages: {total_pages}")
        print(f"Splitting into chunks of {pages_per_split} pages...")
        
        # Calculate number of output files
        num_files = (total_pages + pages_per_split - 1) // pages_per_split
        
        for i in range(num_files):
            # Create a new PDF writer for each chunk
            pdf_writer = PyPDF2.PdfWriter()
            
            # Calculate page range for this chunk
            start_page = i * pages_per_split
            end_page = min((i + 1) * pages_per_split, total_pages)
            
            # Add pages to the writer
            for page_num in range(start_page, end_page):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # Write the output file
            output_filename = os.path.join(
                output_dir, 
                f"{base_name}_part{i+1:02d}_pages{start_page+1}-{end_page}.pdf"
            )
            
            with open(output_filename, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            print(f"Created: {output_filename} (pages {start_page+1}-{end_page})")
        
        print(f"\nSplit complete! {num_files} files created in: {output_dir}")

if __name__ == "__main__":
    input_file = r"AI Engineering Guidebook.pdf"
    
    # You can adjust pages_per_split as needed (default is 50)
    split_pdf(input_file, pages_per_split=50)
