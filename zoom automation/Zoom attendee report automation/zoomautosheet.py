import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('deep-cascade-424606-n5-a591513f2e51.json', scope)

# Authorize the clientsheet 
client = gspread.authorize(creds)

# List all accessible spreadsheets
spreadsheet_list = client.openall()
print("Spreadsheets accessible by the service account:")
for spreadsheet in spreadsheet_list:
    print(spreadsheet.title)


# Open the spreadsheet
spreadsheet_name = "ZOOM AUTO sheet"
spreadsheet = client.open(spreadsheet_name)

# Select the first sheet
sheet = spreadsheet.sheet1

# Load the CSV data into a DataFrame
csv_file = '88478605779 - Attendee Report.csv'
df = pd.read_csv(csv_file)


# Inspect CSV file structure for debugging
with open(csv_file, 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[:10]):  # Print the first 10 lines for inspection
        print(f"Line {i + 1}: {line.strip()}")

# Attempt to read the CSV with pandas
try:
    df = pd.read_csv(csv_file, delimiter=',')  # Adjust the delimiter if necessary
except pd.errors.ParserError as e:
    print(f"ParserError: {e}")
    print("Possible data inconsistency in the CSV file. Printing the first few lines for inspection:")
    with open(csv_file, 'r') as f:
        for i, line in enumerate(f):
            print(f"Line {i + 1}: {line.strip()}")
    # Optionally, re-raise the exception or handle it as needed
    raise e

# Replace NaN values with empty strings
df.fillna('', inplace=True)

     


# Convert DataFrame to a list of lists
data = df.values.tolist()

# Add headers (optional)
header = df.columns.values.tolist()
data.insert(0, header)

# Clear the existing sheet
sheet.clear()

# Update the sheet with new data
sheet.update('A1', data)

print("Data successfully copied from CSV to Google Spreadsheet")

