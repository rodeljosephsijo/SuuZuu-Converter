import os
import asyncio
from PIL import Image
import pandas as pd
from pdf2docx import Converter
import pillow_heif
import subprocess
import fitz
import zipfile

# Enable HEIC decoding for iOS photos
pillow_heif.register_heif_opener()

def convert_pdf_to_word(input_path: str, output_path: str) -> str:
    """Converts a PDF file to a Word (.docx) document."""
    cv = Converter(input_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()
    return output_path

def convert_image_to_pdf(input_path: str, output_path: str) -> str:
    """Converts various image formats to a PDF document."""
    image = Image.open(input_path).convert("RGB")
    image.save(output_path, "PDF")
    return output_path

def convert_image_format(input_path: str, output_path: str, target_format: str) -> str:
    """Converts images between formats (e.g., PNG to JPG)."""
    image = Image.open(input_path)
    if target_format.upper() in ["JPG", "JPEG"]:
        image = image.convert("RGB") # JPG does not support transparency
    image.save(output_path, target_format.upper())
    return output_path

def convert_csv_to_excel(input_path: str, output_path: str) -> str:
    """Converts a CSV spreadsheet to an Excel (.xlsx) workbook."""
    df = pd.read_csv(input_path)
    df.to_excel(output_path, index=False)
    return output_path

def convert_excel_to_csv(input_path: str, output_path: str) -> str:
    """Converts an Excel workbook to a CSV spreadsheet."""
    df = pd.read_excel(input_path)
    df.to_csv(output_path, index=False)
    return output_path

def convert_word_to_pdf(input_path: str, output_path: str) -> str:
    """Converts a Word (.docx) document to PDF using LibreOffice (Linux-compatible)."""
    output_dir = os.path.dirname(output_path) or "."
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", output_dir, input_path],
        check=True, timeout=60
    )
    generated = os.path.join(output_dir, os.path.splitext(os.path.basename(input_path))[0] + ".pdf")
    if generated != output_path:
        os.rename(generated, output_path)
    return output_path

def convert_pdf_to_zip(input_path: str, output_path: str) -> str:
    """Converts a PDF to a ZIP archive containing PNG images of each page."""
    pdf_document = fitz.open(input_path)
    
    # Open a new ZIP file in write mode
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            # Render page to an image (dpi=150 keeps file sizes reasonable)
            pix = page.get_pixmap(dpi=150)
            image_bytes = pix.tobytes("png")
            
            # Write the image bytes directly into the ZIP archive
            image_filename = f"page_{page_num + 1}.png"
            zipf.writestr(image_filename, image_bytes)
            
    pdf_document.close()
    return output_path