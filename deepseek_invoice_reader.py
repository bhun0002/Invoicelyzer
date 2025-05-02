import os
import pytesseract
import requests
from pdf2image import convert_from_path
from PIL import Image

# DeepSeek LLM API (hosted free on Hugging Face Inference endpoint)
API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-llm-7b-chat"
HEADERS = {"Authorization": f"Bearer YOUR_HUGGINGFACE_API_KEY"}  # Replace with real token

def convert_pdf_to_text(pdf_path):
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    text = pytesseract.image_to_string(images[0])
    return text

def ask_deepseek(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "do_sample": False
        }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()[0]["generated_text"]

def extract_invoice_fields(ocr_text):
    prompt = f"""
You are an intelligent assistant. Extract the following fields from the invoice text:
- Invoice Number
- Date
- Issuer
- Recipient
- Total Amount
- Address

Invoice text:
{ocr_text}
"""
    return ask_deepseek(prompt)

def process_invoices(folder_path):
    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            print(f"\n📄 Processing: {file}")
            pdf_path = os.path.join(folder_path, file)
            text = convert_pdf_to_text(pdf_path)
            result = extract_invoice_fields(text)
            print(result)

    print("\n🎯 All invoices processed.")

if __name__ == "__main__":
    folder = input("Enter folder path containing PDF invoices: ").strip()
    if os.path.isdir(folder):
        process_invoices(folder)
    else:
        print("❌ Folder not found.")
