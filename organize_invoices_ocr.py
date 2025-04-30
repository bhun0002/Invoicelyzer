import os
import re
import shutil
from PIL import Image
from pdf2image import convert_from_path
import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel

# Load Donut processor and model
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model.eval()

def convert_pdf_to_image(pdf_path):
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    return images[0].convert("RGB")

def extract_fields_with_donut(image):
    # Donut prompt
    task_prompt = "<s_docvqa><s_question>Extract all invoice information</s_question><s_answer>"
    encoding = processor(images=image, return_tensors="pt")
    pixel_values = encoding.pixel_values
    decoder_input_ids = processor.tokenizer(task_prompt, return_tensors="pt").input_ids

    with torch.no_grad():
        generated = model.generate(
            pixel_values,
            decoder_input_ids=decoder_input_ids,
            max_length=512,
            early_stopping=True,
            pad_token_id=processor.tokenizer.pad_token_id
        )

    result = processor.batch_decode(generated, skip_special_tokens=True)[0]

    # Attempt to extract known fields from result string
    issuer = re.search(r'(Issuer|From)\s*[:\-]?\s*(.*?)(?=\\n|$)', result, re.IGNORECASE)
    recipient = re.search(r'(Recipient|To|BILL TO)\s*[:\-]?\s*(.*?)(?=\\n|$)', result, re.IGNORECASE)
    location = re.search(r'(Location|Address)\s*[:\-]?\s*(.*?)(?=\\n|$)', result, re.IGNORECASE)
    invoice_number = re.search(r'\b\d{5,}/\d{2,4}\b', result)

    issuer_val = issuer.group(2).strip() if issuer else None
    recipient_val = recipient.group(2).strip() if recipient else None
    location_val = location.group(2).strip() if location else None
    invoice_val = invoice_number.group(0).strip() if invoice_number else None

    return issuer_val, recipient_val, invoice_val, location_val, result

def organize_invoice(pdf_path, output_dir):
    image = convert_pdf_to_image(pdf_path)
    issuer, recipient, invoice_number, location, raw_output = extract_fields_with_donut(image)

    print("\n📜 Donut Raw Output:\n" + raw_output)
    print(f"\n📦 Extracted Fields:\n  Issuer: {issuer}\n  Recipient: {recipient}\n  Location: {location}\n  Invoice No: {invoice_number}")

    if not all([issuer, recipient, invoice_number]):
        print(f"⚠️ Skipping {pdf_path}: Missing required fields.\n")
        return

    # Clean strings
    safe_issuer = re.sub(r'[^\w\s\-]', '', issuer).strip().replace(" ", "_")
    safe_recipient = re.sub(r'[^\w\s\-]', '', recipient).strip().replace(" ", "_")
    safe_location = re.sub(r'[^\w\s\-]', '', location).strip().replace(" ", "_") if location else "Unknown"
    safe_invoice = invoice_number.replace("/", "-")

    # Folder structure
    target_dir = os.path.join(output_dir, safe_recipient, safe_location)
    os.makedirs(target_dir, exist_ok=True)

    new_filename = f"{safe_issuer}_{safe_invoice}.pdf"
    target_path = os.path.join(target_dir, new_filename)

    shutil.copy(pdf_path, target_path)
    print(f"✅ Moved {os.path.basename(pdf_path)} --> {target_path}\n")

def main():
    input_dir = input("Enter path to your invoices folder: ").strip()
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            organize_invoice(pdf_path, output_dir)

    print("🎯 All PDFs processed.")

if __name__ == "__main__":
    main()
