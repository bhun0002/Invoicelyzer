from fpdf import FPDF
import os
import random
from datetime import datetime

# Setup
output_folder = "real_invoices"
os.makedirs(output_folder, exist_ok=True)

# Example invoice data
client_name = "Fiona Gallagher"
client_company = "Beta Solutions"
invoice_number = "INV-1008"
invoice_date = datetime.now().strftime("%Y-%m-%d")
invoice_amount = 299.99
items = [
    ("Website Development", 1, 200),
    ("Monthly Maintenance", 1, 99.99)
]

# Create PDF
pdf = FPDF()
pdf.add_page()

# Your Company Details
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, "Your Company Name", ln=True)

pdf.set_font("Arial", size=12)
pdf.cell(0, 10, "123 Business Rd", ln=True)
pdf.cell(0, 10, "Business City, BC 54321", ln=True)
pdf.cell(0, 10, "Email: info@yourcompany.com", ln=True)
pdf.ln(10)

# Invoice Details on the Right
pdf.set_xy(130, 20)
pdf.cell(0, 10, f"Invoice #: {invoice_number}", ln=True)
pdf.set_xy(130, 30)
pdf.cell(0, 10, f"Date: {invoice_date}", ln=True)
pdf.ln(20)

# Bill To
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "Bill To:", ln=True)
pdf.set_font("Arial", size=12)
pdf.cell(0, 10, client_name, ln=True)
pdf.cell(0, 10, client_company, ln=True)
pdf.ln(10)

# Itemized list
pdf.set_font("Arial", 'B', 12)
pdf.cell(80, 10, "Item", border=1)
pdf.cell(30, 10, "Quantity", border=1)
pdf.cell(30, 10, "Price", border=1)
pdf.cell(40, 10, "Total", border=1, ln=True)

pdf.set_font("Arial", size=12)
for item, qty, price in items:
    pdf.cell(80, 10, item, border=1)
    pdf.cell(30, 10, str(qty), border=1)
    pdf.cell(30, 10, f"${price:.2f}", border=1)
    pdf.cell(40, 10, f"${qty * price:.2f}", border=1, ln=True)

pdf.ln(10)
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, f"Total Amount Due: ${invoice_amount:.2f}", ln=True)

pdf.ln(20)
pdf.set_font("Arial", 'I', 12)
pdf.cell(0, 10, "Thank you for your business!", ln=True, align="C")

# Save PDF
file_path = os.path.join(output_folder, f"{invoice_number}.pdf")
pdf.output(file_path)

print(f"✅ Realistic Invoice PDF saved at: {file_path}")