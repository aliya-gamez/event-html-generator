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
script_info() #comment out if needed

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
df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%Y") # convert string to datetime object
df = df.sort_values(by="Date",ascending=True) # sorts dataframe chronologically by date

# Function to remove dates that already occurred
def remove_past_dates(df):
    today = datetime.now().date()
    removed_dt = df[df['Date'].dt.date >= today]
    return removed_dt
df = remove_past_dates(df)

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
    
    # Get CSS class for event type
    event_type = row.iloc[columns["event_type"]]
    css_class = event_css_classes.get(event_type, "unknown")

    # Format HTML using f-string
    html = f"""
            <li class="item {css_class}">
                <div class="main">
                    <div class="name">{row.iloc[columns["name"]]}</div>
                    <div class="date">{formatted_date} @ {row.iloc[columns["location"]]}</div>
                </div>
                <div class="tag">{row.iloc[columns["start_time"]]} - {row.iloc[columns["end_time"]]}</div>
                <div class="desc">{row.iloc[columns["description"]]}</div>
            </li>"""

    # Return statement removing unnessesary whitespace (what strip does)
    return html

# Add new columns in data frame called Month
df['Month'] = df['Date'].dt.to_period('M') # extracts 'period' from date object consisting of month eg. 2024-11
month_groups = df.groupby('Month') # groups dataframe by 'Month' column

# Iterates through each grouped month
html_output = ''
print('=== PRINT MONTH GROUPS ===\n') # for console
for month,group in month_groups: # month is '2024-11' or '2024-12' and group is df object
    print(f'''Month:          Dataframe object for {month.strftime('%B, %Y').strip()}''') # for console
    print('\n',group,'\n') # for console

    # Apply current group dataframe and pass through event_csv_to_html to create rows
    html_list_items = "\n".join(group.apply(event_csv_to_html, axis=1))
    month_heading = month.strftime('%B %Y')
    month_html = f"""<!--{month_heading} Events-->
<h4 class="accordion_title">{month_heading} Events</h4>
<div class="attribute-answer accordion_content">
    <div class="events-cal-ag">
        <ul class="list">{html_list_items}
        </ul>
    </div>
</div>"""

    # Add current month to final html output
    html_output += f"""\n{month_html}"""
    html_output = "\n".join(filter(None, html_output.split("\n"))) # Remove empty lines

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