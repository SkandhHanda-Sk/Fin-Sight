import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import os

# Path to tesseract executable (only for Windows users)
# Uncomment and update this path if needed:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(image_path):
    """Extract text from an image file."""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"Error reading image: {e}"


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF (using both direct text and OCR fallback)."""
    text = ""

    # Try direct text extraction first
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()

    # If text extraction fails (like in scanned PDFs), use OCR
    if not text.strip():
        print("No selectable text found — using OCR...")
        images = convert_from_path(pdf_path)
        for i, img in enumerate(images):
            text += pytesseract.image_to_string(img)

    return text.strip()


# Example usage:
if __name__ == "__main__":
    image_file = "/home/shubhankar/Downloads/Screenshot2024-09-01at2.45.30PM-a3919a880bbc472687252c4e1f4b2e98.png"
    #pdf_file = "sample_document.pdf"

    print("🖼 Extracting text from image...")
    print(extract_text_from_image(image_file))
    print("\n📄 Extracting text from PDF...")
    #print(extract_text_from_pdf(pdf_file))
