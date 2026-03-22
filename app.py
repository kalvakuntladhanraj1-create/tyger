from flask import Flask, request, send_file, abort
from docxtpl import DocxTemplate
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ LOCAL OUTPUT FOLDER (works everywhere)
OUTPUT_DIR = os.path.join(BASE_DIR, "generated")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ================= HEALTH CHECK =================
@app.route("/ping")
def ping():
    return "OK", 200


# ================= HOME =================
@app.route("/")
def home():
    try:
        with open(os.path.join(BASE_DIR, "html", "home.html"), encoding="utf-8") as f:
            return f.read()
    except:
        return "home.html missing", 500


# ================= SALE FORM =================
@app.route("/sale")
def sale_form():
    try:
        with open(os.path.join(BASE_DIR, "html", "sale.html"), encoding="utf-8") as f:
            return f.read()
    except:
        return "sale.html missing", 500


# ================= GIFT FORM =================
@app.route("/gift")
def gift_form():
    try:
        with open(os.path.join(BASE_DIR, "html", "gift.html"), encoding="utf-8") as f:
            return f.read()
    except:
        return "gift.html missing", 500


# ================= GENERATE SALE =================
@app.route("/generate_sale", methods=["POST"])
def generate_sale():
    try:
        data = request.form.to_dict()

        template_path = os.path.join(BASE_DIR, "templates_docx", "sale.docx")
        output_path = os.path.join(OUTPUT_DIR, "sale_report.docx")

        if not os.path.exists(template_path):
            return "sale.docx not found", 500

        doc = DocxTemplate(template_path)
        doc.render(data)
        doc.save(output_path)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Error generating sale report: {str(e)}", 500


# ================= GENERATE GIFT =================
@app.route("/generate_gift", methods=["POST"])
def generate_gift():
    try:
        data = request.form.to_dict()

        template_path = os.path.join(BASE_DIR, "templates_docx", "gift.docx")
        output_path = os.path.join(OUTPUT_DIR, "gift_report.docx")

        if not os.path.exists(template_path):
            return "gift.docx not found", 500

        doc = DocxTemplate(template_path)
        doc.render(data)
        doc.save(output_path)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Error generating gift report: {str(e)}", 500


# ================= RUN SERVER =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ Required for Render
    app.run(host="0.0.0.0", port=port)