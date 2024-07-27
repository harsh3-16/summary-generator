Document Summarizer
This is a Flask-based web application that allows users to upload documents (PDF, DOCX, TXT) and receive a summarized version of the content. The summarization is performed using the Hugging Face transformers library.

Features
Upload PDF, DOCX, or TXT files.
Extract text from the uploaded files.
Summarize the extracted text using a pre-trained model from Hugging Face.

Setup Instructions

Prerequisites
Python 3.7 or higher
Google Colab account
pip package installer
Ngrok account
Latest version of NodeJS

Installation:

Clone the Repository
Copy the contents of the app.py file into a code editor in your local environment.
Copy the contents of the Model.ipynb file into a Google colab notebook.

Note the Ngrok URL in the output and copy it into the app.py file. Remember to add /summarize after the URL.

Set up a React App using create-react-app and copy the contents of client folder.

Add a proxy http://localhost:5000 to package.json file

Run the React app, app.py in separate terminals
Run the Colab notebook.
