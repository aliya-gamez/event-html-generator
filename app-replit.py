# event-html-generator/app.py

from flask import Flask, request, render_template, send_from_directory
from datetime import datetime
import os
import subprocess
import webbrowser
import threading

# Initialize Flask app
app = Flask(__name__)

# Constants
CSV_INPUT_FOLDER = "./csv-input"
HTML_OUTPUT_FOLDER = "./html-output"
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")


# Route for homepage, renders index
@app.route('/')
def index():
    return render_template('index.html')


# Route for file upload then running csv-to-html for conversion
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if upload requests contains file, otherwise get file from request
    if 'file' not in request.files:
        return 'File was not uploaded', 400
    file = request.files['file']

    # Check if file has a name
    if file.filename == '':
        return 'File is empty or has no name', 400

    # Check if uploaded file is a csv file, otherwise return error
    if file and file.filename.endswith('.csv'):
        # Save uploaded file to csv-input folder as current.csv for use within csv-to-html.py
        file_path = os.path.join(CSV_INPUT_FOLDER, 'current.csv')
        file.save(file_path)

        # Call csv-to-html.py script using subprocess to do HTML conversion from current.csv
        try:
            subprocess.run(['python3', 'csv-to-html.py'], check=True)
        except subprocess.CalledProcessError as e:
            return f'Error processign CSV file: {e}', 500

        # Grab generated file from html_output, eg events-2024-11-02.html
        html_file = f'events-{CURRENT_DATE}.html'
        html_file_path = os.path.join(HTML_OUTPUT_FOLDER, html_file)

        # Optionally prompt file download from generated file
        return send_from_directory(HTML_OUTPUT_FOLDER,
                                   html_file,
                                   as_attachment=True)
    return 'Invalid file format (must be .csv)', 400


def open_browser():  # Open browser at flask apps url
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == '__main__':
    #threading.Thread(target=open_browser).start()
    #app.run(debug=False)
    app.run(host="0.0.0.0", port=3000, debug=False)
