from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import requests
import chardet
import fitz  # PyMuPDF for PDF
from docx import Document

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/summarize', methods=['POST'])
def summarize_file():
    data = request.get_json()
    filename = data.get('filename')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    
    try:
        content = extract_text(filepath)
        summary = summarize(content)
        return jsonify({"summary": summary}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.pdf':
        return extract_text_from_pdf(filepath)
    elif ext == '.docx':
        return extract_text_from_docx(filepath)
    elif ext == '.txt':
        return extract_text_from_txt(filepath)
    else:
        raise ValueError("Unsupported file type")

def extract_text_from_pdf(filepath):
    text = ""
    pdf_document = fitz.open(filepath)
    for page in pdf_document:
        text += page.get_text()
    return text

def extract_text_from_docx(filepath):
    doc = Document(filepath)
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    return text

def extract_text_from_txt(filepath):
    with open(filepath, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    
    with open(filepath, 'r', encoding=encoding) as file:
        return file.read()

def summarize(content):
    colab_url = "https://aabb-35-236-139-62.ngrok-free.app/summarize"
    try:
        response = requests.post(colab_url, json={"content": content})
        response.raise_for_status()
        summary = response.json().get('summary', 'Error in summarization')
        return summary
    except requests.RequestException as e:
        return f"Error in API request: {e}"

if __name__ == '__main__':
    app.run(debug=True)
