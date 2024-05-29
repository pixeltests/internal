import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load the CSV file into a pandas DataFrame
# local_path = '/Users/jayanthrasamsetti/Downloads'
csv_file_path = '88478605779 - Attendee Report (2).csv'

df = pd.read_csv(csv_file_path, sep=',', header=11, index_col=False)

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
grouped_df = df.groupby('Email', as_index=False).agg({
    'User Name (Original Name)': 'first',
    'Phone': 'first',
    'Job Title': 'first',
    'Time in Session (minutes)': 'sum',
    'Country/Region Name': 'first'
})

# Apply the function to the 'Time in Session (minutes)' column and create a new column 'Category'
grouped_df['Category'] = grouped_df['Time in Session (minutes)'].apply(categorize_time)

grouped_df.rename(columns={'User Name (Original Name)': 'Name', 'Time in Session (minutes)': 'Time', 'Country/Region Name': 'Country'}, inplace=True)

# # Now grouped_df contains the aggregated data with summed 'Time in Session (minutes)'
grouped_df.sort_values(by='Time',ascending=False)