from fpdf import FPDF
import os
import random

# Sample data
client_names = [
    "Alice Johnson", "Bob Smith", "Charlie Brown",
    "Diana Prince", "Ethan Hunt", "Fiona Gallagher",
    "George Bailey", "Hannah Montana", "Ivan Drago", "Julia Roberts"
]

company_names = [
    "Alpha Corp", "Beta Solutions", "Gamma LLC"
]

invoice_numbers = [f"INV-{1000+i}" for i in range(10)]

# Create output folder
output_folder = "sample_pdfs"
os.makedirs(output_folder, exist_ok=True)

# Create PDFs
for i in range(10):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    random_company = random.choice(company_names)  # pick a random company!

    pdf.cell(200, 10, txt=f"Client Name: {client_names[i]}", ln=True)
    pdf.cell(200, 10, txt=f"Client Company: {random_company}", ln=True)
    pdf.cell(200, 10, txt=f"Invoice Number: {invoice_numbers[i]}", ln=True)

    file_path = os.path.join(output_folder, f"sample_{i+1}.pdf")
    pdf.output(file_path)

print("✅ 10 Sample PDFs generated successfully in the 'sample_pdfs' folder.")
