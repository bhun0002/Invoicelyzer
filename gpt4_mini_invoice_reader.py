import os
import base64
from dotenv import load_dotenv
from pdf2image import convert_from_path
from openai import AzureOpenAI

# Load .env for API key and config
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

client = AzureOpenAI(
    api_key=api_key,
    api_version="2024-12-01-preview",
    azure_endpoint=endpoint
)

def pdf_to_base64_image(pdf_path):
    image = convert_from_path(pdf_path, first_page=1, last_page=1)[0]
    image = image.resize((1024, int(image.height * 1024 / image.width)))  # Resize to save cost
    image.save("temp.jpg")
    with open("temp.jpg", "rb") as f:
        return base64.b64encode(f.read()).decode()

def extract_invoice_details(image_base64):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        max_tokens=500,
        messages=[
            {"role": "system", "content": "You're a financial assistant that extracts structured invoice details from images."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract invoice number, date, issuer, recipient, total, and address from this invoice image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }
        ]
    )
    return response.choices[0].message.content

def process_folder(folder_path):
    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            print(f"\n📄 Processing: {file}")
            pdf_path = os.path.join(folder_path, file)
            img_b64 = pdf_to_base64_image(pdf_path)
            result = extract_invoice_details(img_b64)
            print(result)

if __name__ == "__main__":
    folder = input("Enter folder path containing PDF invoices: ").strip()
    process_folder(folder)
