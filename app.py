from flask import Flask, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", style="B", size=16)
        self.cell(200, 10, "Invoice", ln=True, align="C")

@app.route("/generate_invoice", methods=["POST"])
def generate_invoice():
    data = request.json
    pdf = PDF()
    pdf.add_page()
    
    # **Load a font that supports ₹ symbol**
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.cell(200, 10, f"Invoice for {data['businessName']}", ln=True, align="C")
    pdf.cell(200, 10, f"Customer: {data['customerName']}", ln=True, align="C")

    total_amount = sum(float(item['quantity']) * float(item['price']) for item in data['items'])
    tax_amount = (total_amount * data['taxRate']) / 100
    grand_total = total_amount + tax_amount

    # ✅ **Now ₹ symbol will work**
    pdf.cell(200, 10, f"Total: ₹{total_amount:.2f}", ln=True, align="C")
    pdf.cell(200, 10, f"Tax: ₹{tax_amount:.2f}", ln=True, align="C")
    pdf.cell(200, 10, f"Grand Total: ₹{grand_total:.2f}", ln=True, align="C")

    filename = "invoice.pdf"
    pdf.output(filename)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)


# New Changes