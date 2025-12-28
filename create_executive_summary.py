import fitz  # PyMuPDF
import os
import re

def extract_toc_structure(pdf_path, toc_pages=[3, 4, 5]):
    """Extract the detailed table of contents structure."""
    doc = fitz.open(pdf_path)
    toc_text = ""
    
    for page_num in toc_pages:
        if page_num < len(doc):
            toc_text += doc[page_num].get_text()
    
    doc.close()
    return toc_text

def analyze_toc_for_executive_summary(toc_text):
    """
    Analyze TOC and determine which topics to keep for executive summary.
    Format: (topic_name, start_page, end_page, keep_flag)
    """
    
    # Major sections with their start and end pages
    sections = {
        "LLMs": {
            "start": 7,
            "topics": [
                ("What is an LLM?", 7, 9, True),  # Keep
                ("Need for LLMs", 10, 11, True),  # Keep
                ("What makes an LLM 'large'?", 12, 13, True),  # Keep
                ("How are LLMs built?", 14, 17, True),  # Keep overview only
                ("How to train LLM from scratch?", 18, 22, False),  # Skip - too detailed
                ("How do LLMs work?", 23, 28, True),  # Keep
                ("7 LLM Generation Parameters", 29, 32, False),  # Skip - detailed list
                ("4 LLM Text Generation Strategies", 33, 36, False),  # Skip
                ("3 Techniques to Train An LLM Using Another LLM", 37, 39, False),  # Skip
                ("4 Ways to Run LLMs Locally", 40, 43, False),  # Skip
                ("Transformer vs. Mixture of Experts in LLMs", 44, 48, False),
            ]
        },
        "Prompt Engineering": {
            "start": 50,
            "topics": [
                ("What is Prompt Engineering?", 50, 50, True),  # Keep
                ("3 prompting techniques for reasoning in LLMs", 51, 57, True), 
                ("Verbalized Sampling", 58, 60, False),  # Skip
                ("JSON prompting for LLMs", 61, 65, False),  # Skip
            ]
        },
        "Fine-tuning": {
            "start": 67,
            "topics": [
                ("What is Fine-tuning?", 67, 67, True),  # Keep
                ("Issues with traditional fine-tuning", 68, 69, True),  # Keep
                ("5 LLM Fine-tuning Techniques", 70, 77, False),  # Skip details
                ("Implementing LoRA From Scratch", 78, 79, False),  # Skip - code
                ("How does LoRA work?", 80, 81, False),  # Keep concept only
                ("Implementation", 82, 85, False),  # Skip
                ("Generate Your Own LLM Fine-tuning Dataset (IFT)", 86, 91, False),  # Skip
                ("SFT vs RFT", 92, 93, False),
                ("Build a Reasoning LLM using GRPO", 94, 105, False),  # Skip hands-on
            ]
        },
        "RAG": {
            "start": 106,
            "topics": [
                ("What is RAG?", 106, 106, True),  # Keep
                ("What are vector databases?", 107, 108, True),  # Keep
                ("The purpose of vector databases in RAG", 109, 112, False),
                ("Workflow of a RAG system", 113, 117, True),  # Keep
                ("5 chunking strategies for RAG", 118, 123, False),  # Skip details
                ("Prompting vs. RAG vs. Finetuning?", 124, 125, True),
                ("8 RAG architectures", 126, 127, True), 
                ("RAG vs Agentic RAG", 128, 130, True),  # Keep comparison
                ("Traditional RAG vs HyDE", 131, 133, False),  # Skip
                ("Full-model Fine-tuning vs. LoRA vs. RAG", 134, 138, False),  # Keep comparison
                ("RAG vs REFRAG", 139, 140, False),  # Skip
                ("RAG vs CAG", 141, 142, False),  # Skip
            ]
        },
        "Context Engineering": {
            "start": 147,
            "topics": [
                ("What is Context Engineering?", 147, 148, True),  # Keep
                ("Context Engineering for Agents", 149, 156, True),  # Keep
                ("6 Types of Contexts for AI Agents", 157, 157, False),  # Skip detailed list
                ("Build a Context Engineering workflow", 158, 175, False),  # Skip hands-on
            ]
        },
        "AI Agents": {
            "start": 177,
            "topics": [
                ("What is an AI Agent?", 177, 179, True),  # Keep
                ("Agent vs LLM vs RAG", 180, 180, True),  # Keep comparison
                ("Building blocks of AI Agents", 181, 184, True),  # Keep overview
                ("Custom tools", 185, 193, False),
                ("Cooperation", 194, 194, True),
                ("Memory Types in AI Agents", 195, 195, True),  # Keep
                ("Importance of Memory for Agentic Systems", 196, 198, False),  # Skip
                ("5 Agentic AI Design Patterns", 199, 204, True),
                ("React Pattern details", 203, 204, False),
                ("ReAct Implementation from Scratch", 205, 231, False),  # Skip - code
                ("5 Levels of Agentic AI Systems", 232, 234, True),  # Keep overview
                ("30 Must-Know Agentic AI Terms", 235, 239, False),
                ("4 Layers of Agentic AI", 240, 241, True),  # Keep
                ("7 Patterns in Multi-Agent Systems", 242, 254, False),  # Skip details
            ]
        },
        "MCP": {
            "start": 265,
            "topics": [
                ("What is MCP?", 265, 266, True),  # Keep
                ("Why was MCP created?", 267, 268, True),  # Keep
                ("MCP Architecture Overview", 269, 273, True),  # Keep
                ("Tools, Resources and Prompts", 274, 274, True),
                ("Tools, Resources and Prompts Details", 275, 277, False),
                ("API versus MCP", 278, 280, False),  # Keep comparison
                ("MCP versus Function calling", 281, 281, False),  # Skip
                ("6 Core MCP Primitives", 282, 285, False),  # Skip detailed list
                ("Creating MCP Agents", 286, 304, False),  # Skip hands-on
            ]
        },
        "LLM Optimization": {
            "start": 305,
            "topics": [
                ("Why do we need optimization?", 305, 307, True),  # Keep
                ("Model Compression", 308, 317, False),
                ("Regular ML Inference vs. LLM Inference", 318, 325, False),
                ("KV Caching in LLMs", 326, 330, False),  # Skip details
            ]
        },
        "LLM Evaluation": {
            "start": 332,
            "topics": [
                ("G-eval", 332, 334, False),
                ("LLM Arena-as-a-Judge", 335, 336, False),  # Skip
                ("Multi-turn Evals for LLM Apps", 337, 357, False),  # Skip
            ]
        },
        "LLM Deployment": {
            "start": 359,
            "topics": [
                ("Why is LLM Deployment Different?", 359, 360, False),
                ("vLLM: An LLM Inference Engine", 361, 364, False),  # Skip details
                ("LitServe", 365, 369, False),  # Skip
            ]
        },
        "LLM Observability": {
            "start": 371,
            "topics": [
                ("Evaluation vs Observability", 371, 372, False),
                ("Implementation", 373, 384, False),  # Skip
            ]
        }
    }
    
    return sections

def determine_pages_to_keep(sections, original_total_pages):
    """Determine which specific pages to keep for 80% reduction."""
    pages_to_keep_set = set()
    keep_details = []
    
    # Always keep cover and TOC pages (1-6)
    for page in range(1, 7):
        pages_to_keep_set.add(page)
    keep_details.append(("Cover & TOC", list(range(1, 7))))
    
    for section_name, section_data in sections.items():
        section_pages = []
        
        for topic_data in section_data["topics"]:
            topic_name, start_page, end_page, should_keep = topic_data
            
            if should_keep:
                # Add all pages in the range [start_page, end_page] inclusive
                pages_to_add = list(range(start_page, end_page + 1))
                section_pages.extend(pages_to_add)
                pages_to_keep_set.update(pages_to_add)
        
        if section_pages:
            keep_details.append((section_name, sorted(section_pages)))
    
    return sorted(list(pages_to_keep_set)), keep_details

def create_executive_summary_pdf(input_path, output_path, pages_to_keep):
    """Create summary PDF with selected pages."""
    doc = fitz.open(input_path)
    output_doc = fitz.open()
    
    total_pages = len(doc)
    print(f"\nCreating summary from {total_pages} pages...")
    print(f"Keeping {len(pages_to_keep)} pages ({len(pages_to_keep)/total_pages*100:.1f}%)\n")
    
    for page_num in pages_to_keep:
        if page_num <= total_pages:
            output_doc.insert_pdf(doc, from_page=page_num-1, to_page=page_num-1)
            #print(f"Including page {page_num}")
    
    output_doc.save(output_path)
    output_doc.close()
    doc.close()
    
    # File size comparison
    original_size = os.path.getsize(input_path)
    summary_size = os.path.getsize(output_path)
    
    print(f"\n{'='*70}")
    print(f"SUMMARY CREATED")
    print(f"{'='*70}")
    print(f"Original pages: {total_pages}")
    print(f"Summary pages: {len(pages_to_keep)}")
    print(f"Page reduction: {(1 - len(pages_to_keep)/total_pages)*100:.1f}%")
    print(f"\nOriginal size: {original_size/1024/1024:.2f} MB")
    print(f"Summary size: {summary_size/1024/1024:.2f} MB")
    print(f"Size reduction: {(1 - summary_size/original_size)*100:.1f}%")
    print(f"{'='*70}")

def print_executive_summary_plan(sections, keep_details, total_pages):
    """Print what will be included in the executive summary."""
    print("\n" + "="*70)
    print("SUMMARY PLAN (80% REDUCTION TARGET)")
    print("="*70)
    print("\nWHAT WILL BE KEPT:")
    print("-" * 70)
    
    total_kept = 0
    for section_name, pages in keep_details:
        page_list = ", ".join(str(p) for p in pages)
        print(f"\n{section_name}:")
        print(f"  Pages: {page_list} ({len(pages)} pages)")
        total_kept += len(pages)
    
    print("\n" + "="*70)
    print(f"Total pages to keep: {total_kept} out of {total_pages}")
    print(f"Reduction: {(1 - total_kept/total_pages)*100:.1f}%")
    print("="*70)
    
    print("\nCONTENT STRATEGY:")
    print("  ✓ Keep: Definitions, concepts, comparisons, architecture overviews")
    print("  ✗ Skip: Code examples, detailed implementations, numbered lists,")
    print("          sub-bullets, hands-on tutorials, specific tools")
    print("="*70)

if __name__ == "__main__":
    input_file = r"AI Engineering Guidebook.pdf"
    output_file = r"AI Engineering Guidebook_Summary.pdf"
    
    print("STEP 1: Analyzing document structure...")
    
    # Get the document structure
    doc = fitz.open(input_file)
    total_pages = len(doc)
    doc.close()
    
    print(f"Total pages in original document: {total_pages}")
    
    print("\nSTEP 2: Reading table of contents (pages 4, 5, 6)...")
    toc_text = extract_toc_structure(input_file, toc_pages=[3, 4, 5])
    
    print("\nSTEP 3: Analyzing sections and topics...")
    sections = analyze_toc_for_executive_summary(toc_text)
    
    print("\nSTEP 4: Determining pages to keep...")
    pages_to_keep, keep_details = determine_pages_to_keep(sections, total_pages)
    
    # Print the plan
    print_executive_summary_plan(sections, keep_details, total_pages)
    
    # Automatically proceed
    print("\n" + "="*70)
    print("STEP 5: Creating summary PDF...")
    create_executive_summary_pdf(input_file, output_file, pages_to_keep)
    print(f"\n✓ Summary saved to: {output_file}")
