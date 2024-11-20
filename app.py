# event-html-generator/app.py

from flask import Flask, request, render_template, send_from_directory
import subprocess
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Constants
CSV_INPUT_FOLDER = "./csv-input"
HTML_OUTPUT_FOLDER = "./html-output"
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part',400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file',400

    if file and file.filename.endswith('.csv'):
        # Save uploaded file to csv-input folder
        file_path = os.path.join(CSV_INPUT_FOLDER,'current.csv')
        file.save(file_path)

        # Call csv-to-html.py script using subprocess to do HTML conversion
        try:
            subprocess.run(['python3','csv-to-html.py'],check=True)
        except subprocess.CalledProcessError as e:
            return f'Error processign CSV file: {e}',500
        
        # Find generated HTML file
        html_file = f'events-{CURRENT_DATE}.html'
        html_file_path = os.path.join(HTML_OUTPUT_FOLDER,html_file)

        # Return generated html for download
        return send_from_directory(HTML_OUTPUT_FOLDER,html_file,as_attachment=True)
    
    return 'Invalid file format',400

if __name__=='__main__':
    app.run(debug=True)

