# Stable code

# Next enhancements
# 1. Run this on Cloud as a CRON Job
# 2. File needs to read either csv or xlsx
# 3. Add the Lead Score (Perhaps add Linkedin as well)

import pandas as pd
import numpy as np
import csv
import io

# Load the CSV file into a pandas DataFrame
# local_path = '/Users/jayanthrasamsetti/Downloads'

def find_attendee_details_and_read(file_path):
    # Read the file line by line
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    # Find the index of the "Attendee Details" row
    attendee_row_index = -1
    for i, line in enumerate(lines):
        if "Attendee Details" in line:
            attendee_row_index = i
            break

    if attendee_row_index == -1:
        raise ValueError("Attendee Details row not found")

    # Read the file into a DataFrame starting from the row after "Attendee Details"
    df = pd.read_csv(file_path, skiprows=attendee_row_index + 1, index_col=False)
    return df

# Read the first 20 rows of the CSV file after the "Attendee Details" row
# csv_file_path = '88478605779 - Attendee Report (5).csv'
# csv_file_path = '87888674122 - Attendee Report.csv'
csv_file_path = '88478605779 - Attendee Report (12).csv'

df = find_attendee_details_and_read(csv_file_path)

# df.head(30)

df['Time in Session (minutes)'] = pd.to_numeric(df['Time in Session (minutes)'], errors='coerce')

def clean_phone_number(phone):
    # Remove non-numeric characters
    numeric_phone = ''.join(filter(str.isdigit, str(phone)))

    # If the phone number starts with '0', remove it
    if numeric_phone.startswith('0'):
        numeric_phone = numeric_phone[1:]

    # Ensure the phone number has 10 digits
    if len(numeric_phone) == 10:
        return numeric_phone
    else:
        return None  # Return None for invalid phone numbers

#Clean phone number
df['Phone'] = df['Phone'].apply(clean_phone_number)

def categorize_time(minutes):
    if minutes > 90:
        return 'A'
    elif 45 < minutes <= 90:
        return 'B'
    elif 0 <= minutes <= 45:
        return 'C'
    else:
        return 'Unknown'  # In case there are any negative or invalid values

# # Drop not attended
df = df[df['Attended'] != 'No' ]

# Read the CSV file with custom column names
columns_to_drop = ['First Name', 'Last Name', 'Attended', 'Approval Status','Registration Time', 'Join Time', 'Leave Time', 'Is Guest']

# Drop the specified columns
df.drop(columns=columns_to_drop, inplace=True)

# Group the DataFrame by 'Email' and aggregate the data
grouped_df = df.groupby('Phone', as_index=False).agg({
    'User Name (Original Name)': 'first',
    'Email': 'first',
    'Job Title': 'first',
    'Time in Session (minutes)': 'sum',
    'Country/Region Name': 'first'
})

# Apply the function to the 'Time in Session (minutes)' column and create a new column 'Category'
grouped_df['Category'] = grouped_df['Time in Session (minutes)'].apply(categorize_time)

grouped_df.rename(columns={'User Name (Original Name)': 'Name', 'Time in Session (minutes)': 'Time', 'Country/Region Name': 'Country'}, inplace=True)

# # Now grouped_df contains the aggregated data with summed 'Time in Session (minutes)'
grouped_df.sort_values(by='Time',ascending=False)
