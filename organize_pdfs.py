 import os
import shutil
import fitz  # PyMuPDF
import re

def extract_fields(text):
    client_name = re.search(r"Client Name[:\s]+(.+)", text)
    client_company = re.search(r"Client Company[:\s]+(.+)", text)
    invoice_number = re.search(r"Invoice Number[:\s]+(.+)", text)

    return (
        client_name.group(1).strip() if client_name else None,
        client_company.group(1).strip() if client_company else None,
        invoice_number.group(1).strip() if invoice_number else None
    )

def organize_pdfs(root_folder):
    for filename in os.listdir(root_folder):
        if filename.endswith('.pdf'):
            file_path = os.path.join(root_folder, filename)
            doc = fitz.open(file_path)

            text = ""
            for page in doc:
                text += page.get_text()

            client_name, client_company, invoice_number = extract_fields(text)

            if not all([client_name, client_company, invoice_number]):
                print(f"⚠️ Skipping {filename}: Missing fields")
                continue

            safe_company = client_company.replace(" ", "_")
            safe_client_name = client_name.replace(" ", "_")
            safe_invoice_number = invoice_number.replace("/", "-")

            target_dir = os.path.join(root_folder, safe_company)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            new_filename = f"{safe_client_name}_{safe_invoice_number}.pdf"
            target_path = os.path.join(target_dir, new_filename)

            shutil.move(file_path, target_path)
            print(f"✅ Moved {filename} --> {target_path}")

if __name__ == "__main__":
    root_folder = input("Enter the path to your PDFs folder: ").strip()
    organize_pdfs(root_folder)
    print("\n🎯 All PDFs processed.")