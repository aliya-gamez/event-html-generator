#!/usr/bin/env python3
def script_info():
    print("\n=== SCRIPT STARTED ===")
    print("\nTitle:\t\tEvent Excel Sheet to HTML Script")
    print("Developer:\tAliya Gamez")
    print("Description:\tThis script turns the Fall 2024 to Summer 2025 events excel sheet into HTML for staff newsletter.")
    print("Requirements:\t1) Save current semester schedule excel sheet into csv-input folder.\n"
          + "\t\t2) Rename or name CSV file as current.csv. When script is completed it will become the date.\n"
          + "\t\t3) (Windows) Make sure virtual environment is activated for wheel and pandas to work.\n"
          + "\t\t4) (Unix/Linux) Make sure wheel and pandas are installed.\n"
          + "\t\t5) Run main.py, make sure environment is activated for wheel and pandas to work\n")
script_info()

"""
EXAMPLE CSV:
11/7/2024,Presentation,Wellness,CHAW Overview,RBA 0103,8:00 AM,8:30 AM,,Overview of CHAW services for UROP program leaders,TBD,,No,No,Kris Ryan,123-456-7890,XXXX@fsu.edu,General,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

EXAMPLE HTML:
<li class="item present">
    <div class="main">
        <div class="name">CHAW Overview</div>
        <div class="date">Thursday, November 1 @ RBA XXXX</div>
    </div>
    <div class="tag">8:00am - 8:30am</div>
    <div class="desc">Overview of CHAW services for UROP program leaders.</div>
</li>
"""

################## script start ##################

# Imports
import pandas as pd
import shutil as st
from datetime import datetime
import os
import sys

# Constants
CSV_CURRENT_PATH = "./csv-input/current.csv"
CSV_INPUT_FOLDER = "./csv-input"
HTML_OUTPUT_FOLDER = "./html-output"
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

# Check if file needed for script exists, else terminate
if(os.path.exists(CSV_CURRENT_PATH) == False):
    print("Failed:\t\tFile current.csv doesn't exist within csv-input folder. Aborting...\n")
    sys.exit(1) #terminate

# Load DF and sort by Date
df = pd.read_csv(CSV_CURRENT_PATH, encoding="latin1") # load CSV file and skips header row
df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%Y")
df = df.sort_values(by="Date",ascending=True)

# Function to call later into df.apply() and join HTML together for output
def event_csv_to_html(row):
    # Column Event Dictionary (for readibility)
    columns = {
        "date": 0, #A
        "event_type": 1, #B
        "name": 3, # D
        "location": 4, #E
        "start_time": 5, #F
        "end_time": 6, #G
        "description": 8 #I
    }

    # Presentation Topic Type to css class
    event_css_classes = {
        "Tabling": "table",
        "Meeting": "meet",
        "Event": "event",
        "Presentation": "present"
    }

    # Removing Empty Rows: Check for NaN in used columns
    if pd.isna(row.iloc[columns["name"]]) or pd.isna(row.iloc[columns["date"]]) or pd.isna(row.iloc[columns["event_type"]]):
        return ""

    # Date Handling: Parse and format date : "date"
    row_date_object = row.iloc[columns["date"]] #timestamp object
    formatted_date = row_date_object.strftime("%A, %B ") + str(row_date_object.day)  #call integer row_date_object.day as a string instead of using %-d (doesnt work on)

    # Date Handling: Removing Events that Already Occured
    now_date_object = datetime.now()
    if row_date_object.date() < now_date_object.date():
        return ""
    
    # Get CSS class for event type
    event_type = row.iloc[columns["event_type"]]
    css_class = event_css_classes.get(event_type, "unknown")

    # Format HTML using f-string
    html = f"""\t<li class="item {css_class}">
        <div class="main">
            <div class="name">{row.iloc[columns["name"]]}</div>
            <div class="date">{formatted_date} @ {row.iloc[columns["location"]]}</div>
        </div>
        <div class="tag">{row.iloc[columns["start_time"]]} - {row.iloc[columns["end_time"]]}</div>
        <div class="desc">{row.iloc[columns["description"]]}</div>
    </li>"""

    # Return statement removing unnessesary whitespace (what strip does)
    return html

# Apply the function to each CSV row and generate HTML, passing row data into the row parameter of event_csv_to_html
html_list_items = "\n".join(df.apply(event_csv_to_html, axis=1))
html_output = f"""<ul class="list">\n{html_list_items}\n</ul>"""
html_output = "\n".join(filter(None, html_output.split("\n"))) #removes white space (empty lines) from html_output, (a lot is created during removal of empty rows in spreadsheet and events that already occurred)

# Rename current.csv to current date .csv
new_csv_file = "events-" + CURRENT_DATE + ".csv"
new_csv_file_path = os.path.join(CSV_INPUT_FOLDER, new_csv_file)
os.rename(CSV_CURRENT_PATH, new_csv_file_path)
print("Success:\tRenamed " + CSV_CURRENT_PATH + " to " + new_csv_file_path)

# Save the result to an HTML file in the output folder
new_html_file = "events-" + CURRENT_DATE + ".html"
new_html_file_path = os.path.join(HTML_OUTPUT_FOLDER, new_html_file)
with open(new_html_file_path, "w", encoding="utf-8") as file:
    file.write(html_output)
print("Success:\tCreated " + new_html_file_path)

print("\n=== SCRIPT ENDED ===\n")

################## script end ##################



