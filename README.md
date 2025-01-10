# PDF Information Extraction Solution

## Overview
This solution automates the extraction of key information from scanned PDFs, such as company names, company identifiers, and the purpose of the document. It uses OCR and text processing techniques to parse and structure the data into a JSON format with the following fields:
- **Company Name**
- **Company Identifier**
- **Document Purpose** (includes a summary and key terms)

The solution is designed for publicly available gazette documents from the Belgian Gazette Service, which may be in English, French, Dutch, or German.

---

## Prerequisites

1. **Python Version**:
   - This script requires Python 3.8 or above.

2. **Required Python Libraries**:
   - All required libraries are listed in the `requirements.txt` file.

3. **Tesseract OCR**:
   - Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and note the installation path.
   - Ensure the path to the Tesseract executable is updated in the script:
     ```python
     pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
     ```

4. **Poppler Utilities**:
   - For `pdf2image` to work, ensure you have `poppler-utils` installed:
     - On Linux:
       ```bash
       sudo apt-get install poppler-utils
       ```
     - On Windows, download the binary from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/), and add it to your PATH.

---

## File Structure

- **`gazette_info_extractor.py`**: The main Python script for processing PDFs.
- **`requirements.txt`**: A file containing all dependencies for this project.
- **`output.json`**: The JSON file where extracted data is saved.
- Input PDFs should be stored in the appropriate folder and paths updated in the script.

---

## How to Set Up

### Step 1: Clone or Download the Repository
Clone the repository or download the script and related files to your local machine.

### Step 2: Install Dependencies
Run the following command in your terminal to install all dependencies:
```bash
pip install -r requirements.txt
```

Step 3: Configure Tesseract OCR
Ensure Tesseract OCR is installed.
Update the path to the Tesseract executable in the script:

```python
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
```

---

## How to Run
Step 1: Update the File Paths

In the `gazzette_info_extractor.py`, update the list of PDF file paths in the pdf_files variable:

```python
pdf_files = [
    "path/to/your/pdf1.pdf",
    "path/to/your/pdf2.pdf"
]
```

## Step 2: Execute the Script

Run the script from the terminal or your preferred Python IDE:

```python
python gazette_info_extractor.py
```

## Step 3: View the Output

The extracted information will be saved to extracted_information_final.json in the same directory. Open this file to view the structured data.

---

## Example Output

Here’s an example of the JSON output:

```json
[
    {
        "Company Name": "A COMPANY",
        "Company Identifier": "0123 456 789",
        "Document Purpose": "Document Purpose Here"
    }
]
```
---

## Notes

- The solution processes multi-language PDFs (English, French, Dutch, and German).
- Ensure the PDFs are clear and legible for OCR to work effectively.
- Error handling is included to report issues with specific PDFs.

---

## Troubleshooting

- TesseractNotFoundError: Ensure Tesseract OCR is installed, and the correct path is set in the script:

  ```python
  pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
  ```

- Poor OCR Accuracy: Use high-quality PDF scans for better OCR results.

- Missing Dependencies: Reinstall required Python libraries using:

```python
        pip install -r requirements.txt
```

---

## File Structure Overview

Project Directory
│
├── script.py                    # Main Python script
├── requirements.txt             # Python dependencies file
├── extracted_information_final.json  # Output JSON file
└── PDFs                         # Directory containing input PDF files

---

## Dependencies

The required Python libraries are listed in the requirements.txt file:

```python
    pytesseract
    pdf2image
    nltk
    langdetect
```

To install these dependencies, use:

```python
pip install -r requirements.txt
```
