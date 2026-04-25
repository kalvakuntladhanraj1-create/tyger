from flask import Flask, request, send_file
from docxtpl import DocxTemplate
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "generated")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# 🔥 ADDED: Date formatter
def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%m-%Y")
    except:
        return date_str


# ================= HOME =================
@app.route("/")
def home():
    return open(os.path.join(BASE_DIR, "html", "home.html"), encoding="utf-8").read()


# ================= SALE FORM =================
@app.route("/sale")
def sale_form():
    return open(os.path.join(BASE_DIR, "html", "sale.html"), encoding="utf-8").read()


# ================= GIFT FORM =================
@app.route("/gift")
def gift_form():
    return open(os.path.join(BASE_DIR, "html", "gift.html"), encoding="utf-8").read()


# ================= CORE GENERATOR =================
def generate_document(doc_type):
    try:
        print(f"\n🔥 ROUTE HIT: {doc_type.upper()}")

        data = request.form.to_dict()

        # 🔥 ADDED: Convert date format (YYYY-MM-DD → DD-MM-YYYY)
        date_fields = [
            "DATE",
            "DEED_DATE",
            "POSSESSION_DATE",
            "H_T_DATE",
            "EC_DATE"
        ]

        for field in date_fields:
            if field in data and data[field]:
                data[field] = format_date(data[field])

        # 🔥 Fix placeholder mismatch automatically
        if "ASSESSMENT_NO" in data:
            data["Assessment_No"] = data["ASSESSMENT_NO"]

        print("📥 DATA RECEIVED:", data)

        template_file = f"{doc_type}.docx"
        template_path = os.path.join(BASE_DIR, "templates_docx", template_file)

        if not os.path.exists(template_path):
            return f"{template_file} not found", 500

        print("📄 USING TEMPLATE:", template_path)

        filename = f"{doc_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
        output_path = os.path.join(OUTPUT_DIR, filename)

        doc = DocxTemplate(template_path)
        doc.render(data)
        doc.save(output_path)

        print("✅ FILE GENERATED:", filename)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print("❌ ERROR:", str(e))
        return f"Error generating {doc_type} document: {str(e)}", 500


# ================= ROUTES =================
@app.route("/generate_sale", methods=["POST"])
def generate_sale():
    return generate_document("sale")


@app.route("/generate_gift", methods=["POST"])
def generate_gift():
    return generate_document("gift")


# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
