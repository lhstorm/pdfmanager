# PDF Manager

## Overview
PDF Namer is a Python tool that automatically renames PDF files based on their content using a local LLM (Large Language Model). It extracts text from PDFs and generates descriptive filenames that reflect the document's content.

## Features
- Automatically extracts text content from PDF files
- Uses Ollama's local LLM to generate descriptive filenames. **Default model is Llama 3.2. Please ensure it is installed.**
- Handles multiple PDFs in a directory
- Ensures safe filename formatting (lowercase, underscores, no special characters)
- Prevents accidental file overwrites

## Installation and Usage

### Clone the repository

```bash

git clone https://github.com/yourusername/pdfnamer.git
cd pdfnamer
```

### Create a virtual environment and install dependencies
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Run the script

```bash
python3 pdfnamer.py
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

