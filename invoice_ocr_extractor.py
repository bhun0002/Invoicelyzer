import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Optional: Set tesseract path manually (if not in system PATH)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    image_paths = []

    for i, img in enumerate(images):
        img_path = f"{pdf_path}_page_{i+1}.png"
        img.save(img_path, 'PNG')
        image_paths.append(img_path)

    return image_paths

def extract_text_from_images(image_paths):
    extracted_text = ""
    for img_path in image_paths:
        print(f"🔍 OCR on: {img_path}")
        text = pytesseract.image_to_string(Image.open(img_path))
        extracted_text += f"\n--- Page {image_paths.index(img_path)+1} ---\n{text}"
    return extracted_text

def process_invoice(pdf_path):
    images = convert_pdf_to_images(pdf_path)
    text = extract_text_from_images(images)
    print("\n📝 Extracted Text:")
    print(text)

if __name__ == "__main__":
    folder = input("Enter folder path containing PDF invoices: ").strip()
    if not os.path.isdir(folder):
        print("❌ Folder not found.")
    else:
        for file in os.listdir(folder):
            if file.lower().endswith(".pdf"):
                print(f"\n📄 Processing: {file}")
                process_invoice(os.path.join(folder, file))
