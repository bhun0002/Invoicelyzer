import os
import shutil
import fitz  # PyMuPDF
import re

def extract_fields(text):
    lines = text.splitlines()
    issuer_name = None         # e.g., Deval Test (used in file name)
    bill_to_company = None     # e.g., Rabbie Ltd. (used as folder name)
    invoice_number = None      # e.g., 225689/23

    # Extract invoice number
    invoice_match = re.search(r'Invoice No[:\s]+([A-Za-z0-9/-]+)', text)
    if invoice_match:
        invoice_number = invoice_match.group(1).strip()

    # Locate issuer and bill-to company from expected positions
    for idx, line in enumerate(lines):
        if "Invoice No" in line:
            if idx + 1 < len(lines):
                issuer_name = lines[idx + 1].strip()
            if idx + 2 < len(lines):
                bill_to_company = lines[idx + 2].strip()
            break

    return issuer_name, bill_to_company, invoice_number

def organize_pdfs(root_folder):
    for filename in os.listdir(root_folder):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(root_folder, filename)
            doc = fitz.open(file_path)

            text = ""
            for page in doc:
                text += page.get_text()

            issuer_name, bill_to_company, invoice_number = extract_fields(text)

            if not all([issuer_name, bill_to_company, invoice_number]):
                print(f"⚠️ Skipping {filename}: Missing fields")
                continue

            # Clean up for filesystem-safe names
            safe_folder = re.sub(r'[^\w\- ]', '', bill_to_company).replace(" ", "_")
            safe_issuer = re.sub(r'[^\w\- ]', '', issuer_name).replace(" ", "_")
            safe_invoice = invoice_number.replace("/", "-")

            # Create output directory
            target_dir = os.path.join(root_folder, safe_folder)
            os.makedirs(target_dir, exist_ok=True)

            # Construct final file name
            new_filename = f"{safe_issuer}_{safe_invoice}.pdf"
            target_path = os.path.join(target_dir, new_filename)

            # Move and rename
            shutil.move(file_path, target_path)
            print(f"✅ Moved {filename} --> {target_path}")

if __name__ == "__main__":
    root_folder = input("Enter the path to your PDFs folder: ").strip()
    organize_pdfs(root_folder)
    print("\n🎯 All PDFs processed.")