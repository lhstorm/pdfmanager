import os
import glob
import re
from PyPDF2 import PdfReader
from ollama import chat, ChatResponse

def get_pdf_content(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def generate_new_name(pdf_text: str) -> str:
    """Use the local LLM to propose a descriptive filename for the PDF based on its content."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that, given the content of a PDF file, "
                "will propose a succinct yet descriptive filename for the PDF. "
                "Return only the filename, without quotes or explanation. "
                "Use lowercase letters, underscores between words, and end with .pdf. "
                "Do not include spaces or special characters (other than underscores)."
            )
        },
        {
            "role": "user",
            "content": f"PDF content:\n{pdf_text}\n\nGenerate a short descriptive filename based on the content."
        }
    ]

    response: ChatResponse = chat(model='llama3.2', messages=messages)
    proposed_name = response.message.content.strip()
    # Sanitize filename: remove problematic characters and ensure .pdf extension
    proposed_name = re.sub(r'[^a-z0-9_]+', '_', proposed_name.lower()).strip('_')
    if not proposed_name.endswith('.pdf'):
        proposed_name += '.pdf'
    return proposed_name

def rename_pdfs_in_directory(directory: str):
    pdf_files = glob.glob(os.path.join(directory, '*.pdf'))
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        pdf_text = get_pdf_content(pdf_file)
        
        if not pdf_text.strip():
            print(f"No text found in {pdf_file}. Skipping this file.")
            continue
        
        new_name = generate_new_name(pdf_text)
        new_path = os.path.join(directory, new_name)
        
        # If a file with the new name already exists, skip to avoid overwriting
        if os.path.exists(new_path):
            print(f"A file with the name {new_name} already exists. Skipping rename.")
            continue
        
        os.rename(pdf_file, new_path)
        print(f"Renamed {pdf_file} to {new_name}.")

if __name__ == "__main__":
    import sys
    target_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    rename_pdfs_in_directory(target_directory)
    