import os
import base64
import openai
from dotenv import load_dotenv
from PIL import Image
from pdf2image import convert_from_path

# Load environment variables
load_dotenv()

# Azure OpenAI credentials
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # e.g. https://your-resource.openai.azure.com/
openai.api_type = "azure"
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")  # e.g. 2024-02-15-preview
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g. gpt-4o

def extract_invoice_details_from_image(image_path):
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    try:
        response = openai.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        { "type": "text", "text": "Extract invoice number, date, issuer, recipient, total amount, and address from this invoice." },
                        { "type": "image_url", "image_url": { "url": f"data:image/png;base64,{base64_image}" } }
                    ],
                }
            ],
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error:\n\n{e}"

def convert_pdf_to_image(pdf_path):
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    temp_path = pdf_path.replace(".pdf", "_temp.png")
    images[0].save(temp_path, "PNG")
    return temp_path

def process_all_pdfs_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"\n📄 Processing: {filename}")
            image_path = convert_pdf_to_image(pdf_path)
            result = extract_invoice_details_from_image(image_path)
            print(result)

    print("\n🎯 All invoices processed.")
    print(deployment_name)

if __name__ == "__main__":
    folder = input("Enter folder path containing PDF invoices: ").strip()
    if os.path.isdir(folder):
        process_all_pdfs_in_folder(folder)
    else:
        print("❌ Folder not found.")
