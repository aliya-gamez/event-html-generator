import pandas as pd
import shutil as st
from datetime import datetime
import os

CSV_CURRENT_PATH = "csv-input/current.csv"
CSV_INPUT_FOLDER = "csv-input"
HTML_OUTPUT_FOLDER = "html-output"
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

# Variables:
new_html_file = "events-" + CURRENT_DATE + ".html"
new_html_file_path = os.path.join(HTML_OUTPUT_FOLDER, new_html_file)
new_csv_file = "events-" + CURRENT_DATE + ".csv"
new_csv_file_path = os.path.join(CSV_INPUT_FOLDER, new_csv_file)

# For testing, comment out if not needed
if os.path.exists(CSV_CURRENT_PATH):
  print("\nFailed:\tThere is already a current.csv file")
else:
  st.copy(new_csv_file_path, CSV_CURRENT_PATH)
  print("\nSuccess:\tRecreated current.csv")

# Delete FIles:
if os.path.exists(new_csv_file_path):
  os.remove(new_csv_file_path)
  print("Success:\tRemoved csv file")
else:
  print("Failed:\tThe CSV file does not exist")

if os.path.exists(new_html_file_path):
  os.remove(new_html_file_path)
  print("Success:\tRemoved html file\n")
else:
  print("Failed:\tThe HTML file does not exist\n")



