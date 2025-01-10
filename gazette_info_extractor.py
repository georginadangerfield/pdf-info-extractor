import os
import re
import json
from pdf2image import convert_from_path
import pytesseract
from langdetect import detect

import nltk

# Ensure 'punkt' is downloaded and available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', force=True)

from nltk.tokenize import sent_tokenize

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    return "\n".join(pytesseract.image_to_string(img, lang="eng+fra+deu+nld") for img in images)

# Function to summarise text details
def summarise_details(details):
    if not details:
        return ""

    full_text = re.sub(r"[^\w\s,.]{3,}", "", " ".join(details).strip())
    full_text = re.sub(r"\s{2,}", " ", full_text)

    try:
        if detect(full_text) not in ["en", "fr", "nl", "de"]:
            return "Text removed due to unexpected language."
    except Exception:
        return "Text removed due to language detection failure."

    sentences = sent_tokenize(full_text)
    return " ".join(sentences[:3])  # Fixed summary length

# Function to parse text and extract relevant information
def parse_information(extracted_text):
    keywords = {
        "company_name": ["en entier", "en entler", "en enter"],
        "company_identifier": ["N° d'entreprise", "N’ dentreprise", "N° @entreprise", "N° dientreprise"],
        "document_purpose": ["Objet de Pacte", "Objet de lacte", "Qbiet de Vacte", "Objet de l’acte", "' Qbjet de Pacte "]
    }
    key_terms = [
        "appointment", "resignation", "director", "transfer of shares", 
        "administrateur", "cession", "siége social"
    ]

    company_name, company_identifier, document_purpose = None, None, None
    capture_details = False
    extracted_key_terms = []
    details = []

    for line in map(str.strip, extracted_text.split("\n")):
        if not line:
            continue

        # Specific override for a known misread
        if "POF 86426" in line:
            company_identifier = "761786926"
        elif any(keyword in line.lower() for keyword in keywords["company_name"]):
            company_name = re.sub(r"[\(\{].*?[\)\}]|^[^\w\d]+|[^\w\d]+$", "", line.split(":")[-1].strip())
        elif any(keyword in line for keyword in keywords["company_identifier"]):
            numbers = re.findall(r"\d{3,}", line)
            company_identifier = " ".join(numbers) if numbers else None
        elif any(keyword in line for keyword in keywords["document_purpose"]):
            document_purpose = re.split(r'[\.\!\?]', line.split(":")[-1].strip())[0]
            capture_details = True

        # Capture potential key terms related to the purpose
        for term in key_terms:
            if term in line.lower():
                extracted_key_terms.append(term)

        # Capture additional details following purpose detection
        if capture_details:
            if line:
                details.append(line)
            else:
                capture_details = False

    # Format Document Purpose with Summary and Key Terms
    summary = summarise_details(details)
    if document_purpose:
        document_purpose += f" | Summary: {summary} | Key Terms: {', '.join(set(extracted_key_terms))}"

    return {
        "Company Name": company_name,
        "Company Identifier": company_identifier,
        "Document Purpose": document_purpose
    }

# Function to process multiple PDFs and save the output
def process_pdfs(file_paths, output_file):
    output = []
    for path in file_paths:
        try:
            text = extract_text_from_pdf(path)
            info = parse_information(text)
            output.append(info)
        except Exception as e:
            output.append({"Error": str(e), "File": os.path.basename(path)})

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(output, json_file, indent=4, ensure_ascii=False)
    print(f"Extraction complete. Results saved to {output_file}")

# Main block to execute the script
if __name__ == "__main__":
    pdf_files = [
        "C:/Users/GeorginaDangerfield/OneDrive - Technical Professionals Limited (1)/Georgina's Documents/Personal/BE_GAZETTE_PDFS 1 (2)/24000001.pdf",
        "C:/Users/GeorginaDangerfield/OneDrive - Technical Professionals Limited (1)/Georgina's Documents/Personal/BE_GAZETTE_PDFS 1 (2)/24000002.pdf",
        "C:/Users/GeorginaDangerfield/OneDrive - Technical Professionals Limited (1)/Georgina's Documents/Personal/BE_GAZETTE_PDFS 1 (2)/24000003.pdf",
        "C:/Users/GeorginaDangerfield/OneDrive - Technical Professionals Limited (1)/Georgina's Documents/Personal/BE_GAZETTE_PDFS 1 (2)/24000004.pdf",
        "C:/Users/GeorginaDangerfield/OneDrive - Technical Professionals Limited (1)/Georgina's Documents/Personal/BE_GAZETTE_PDFS 1 (2)/24000005.pdf",
        "C:/Users/GeorginaDangerfield/OneDrive - Technical Professionals Limited (1)/Georgina's Documents/Personal/BE_GAZETTE_PDFS 1 (2)/24000006.pdf",
        "C:/Users/GeorginaDangerfield/OneDrive - Technical Professionals Limited (1)/Georgina's Documents/Personal/BE_GAZETTE_PDFS 1 (2)/24000007.pdf",
        "C:/Users/GeorginaDangerfield/OneDrive - Technical Professionals Limited (1)/Georgina's Documents/Personal/BE_GAZETTE_PDFS 1 (2)/24000008.pdf",
        "C:/Users/GeorginaDangerfield/OneDrive - Technical Professionals Limited (1)/Georgina's Documents/Personal/BE_GAZETTE_PDFS 1 (2)/24000009.pdf",
        "C:/Users/GeorginaDangerfield/OneDrive - Technical Professionals Limited (1)/Georgina's Documents/Personal/BE_GAZETTE_PDFS 1 (2)/24000010.pdf"
    ]
    output_json = "extracted_information_final.json"
    process_pdfs(pdf_files, output_json)
