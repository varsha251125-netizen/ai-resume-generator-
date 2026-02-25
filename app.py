import os
from flask import Flask, render_template, request, send_file
from dotenv import load_dotenv
from openai import OpenAI
from fpdf import FPDF

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ===============================
# AI Resume Generator Function
# ===============================
def generate_resume(data):
    prompt = f"""
    Create a professional ATS-friendly resume using the following details.

    Name: {data['name']}
    Email: {data['email']}
    Phone: {data['phone']}
    Education: {data['education']}
    Experience: {data['experience']}
    Skills: {data['skills']}
    Projects: {data['projects']}
    Target Job Role: {data['job_role']}

    Requirements:
    - Use strong action verbs
    - Make it professional
    - Use bullet points for experience
    - Add professional summary
    - Make it ATS optimized
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


# ===============================
# Routes
# ===============================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    form_data = request.form.to_dict()
    resume_content = generate_resume(form_data)
    return render_template("result.html", resume=resume_content)


@app.route("/download", methods=["POST"])
def download():
    resume_text = request.form["resume"]

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    for line in resume_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    file_path = "Generated_Resume.pdf"
    pdf.output(file_path)

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
