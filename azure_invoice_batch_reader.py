import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your Azure Form Recognizer endpoint and key
AZURE_ENDPOINT = os.getenv("AZURE_FORMRECOGNIZER_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_FORMRECOGNIZER_KEY")
API_VERSION = "2023-07-31"
MODEL = "prebuilt-invoice"

# Headers for the request
headers = {
    "Ocp-Apim-Subscription-Key": AZURE_KEY,
    "Content-Type": "application/pdf"
}

def analyze_invoice(file_path):
    analyze_url = f"{AZURE_ENDPOINT}/formrecognizer/documentModels/{MODEL}:analyze?api-version={API_VERSION}"

    with open(file_path, "rb") as f:
        response = requests.post(analyze_url, headers=headers, data=f)
    
    if response.status_code != 202:
        print(f"❌ Error submitting {file_path}: {response.status_code} - {response.text}")
        return

    # Get the operation-location URL to poll
    operation_location = response.headers["operation-location"]

    # Poll for result
    while True:
        result_response = requests.get(operation_location, headers={"Ocp-Apim-Subscription-Key": AZURE_KEY})
        result_json = result_response.json()

        status = result_json.get("status")
        if status == "succeeded":
            print(f"\n✅ {os.path.basename(file_path)} processed successfully.")
            print_invoice_fields(result_json)
            break
        elif status == "failed":
            print(f"❌ Analysis failed for {file_path}")
            break
        time.sleep(1)

# def print_invoice_fields(result_json):
#     fields = result_json["analyzeResult"]["documents"][0]["fields"]
#     for key, value in fields.items():
#         content = value.get("content")
#         confidence = value.get("confidence", 0)
#         if content:
#             print(f"- {key}: {content} (confidence: {confidence:.2f})")

def print_invoice_fields(result_json):
    documents = result_json.get("analyzeResult", {}).get("documents", [])
    if not documents:
        print("⚠️ No document fields found.")
        return

    fields = documents[0].get("fields", {})
    for key in sorted(fields.keys()):
        field = fields[key]
        content = field.get("content", "").strip()
        confidence = field.get("confidence", 0)
        if content:
            print(f"- {key}: {content} (confidence: {confidence:.2f})")

def process_folder():
    folder_path = input("📁 Enter folder path containing PDFs: ").strip()
    if not os.path.isdir(folder_path):
        print("❌ Invalid folder path.")
        return

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"\n📄 Processing: {filename}")
            analyze_invoice(file_path)

if __name__ == "__main__":
    process_folder()
