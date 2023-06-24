# Script to filter the information I want from syslog file
# I would like to retrieve the logs about system boot/reboot/turn off
# Jun  4 21:38:15 mrrari14 systemd[973]: Reached target Shutdown.
# Jun 16 10:25:19 mrrari14 kernel: [    0.045535] Booting paravirtualized kernel on bare hardware
# Jun 16 12:02:58 mrrari14 systemd-sleep[25557]: Entering sleep state 'suspend'...

# Each line the code reads represents 1 read request to google sheets api

# Import libs to communicate with google api to access spreadsheets
import os
from time import sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define file location
file_path = '/var/log/syslog'
user_name = 'mrrari14'
sys_prefix = 'systemd'
system_logs = []
shutdown_logs = []
booting_logs = []
sleep_logs = []

# Functions
def filter_shutdown():
    print('This can take a minute, please dont exit the program.')
    sleep(60)
    for line in system_logs:
        if 'Reached target Shutdown' in line:
            split_line = line.split()
            shutdown_log = split_line[0] + ' ' + split_line[1] + ' ' + split_line[2] + ' ' + split_line[7]
            shutdown_logs.append(shutdown_log)

    logs_batch = 60
    batch_items = shutdown_logs[:logs_batch]

    for item in batch_items:
        split_item = item.split()
        date = split_item[0] + ' ' + split_item[1]
        time = split_item[2]
        process = split_item[3]
    # Write date to sheets
        # Construct the row to be appended
        row = [date, time, process]
        # Determine the range to append the row
        table_range = 'A' + str(sheet.row_count + 1) + ':C' + str(sheet.row_count + 1)
        # Append the row to the sheet
        sheet.append_row(row, value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS', table_range=table_range)
        # sheet.format('C', {
        #     'backgroundColor': {
        #         'red': 1,
        #         'green': 0,
        #         'blue': 0,
        #         'alpha': 0.5
        #     },
        #     'textFormat': {
        #         'foregroundColor': {
        #             'red': 255,
        #             'green': 255,
        #             'blue': 255
        #         }
        #     },
        # })

def filter_boot():
    print('This can take a minute, please dont exit the program.')
    sleep(60)
    for line in system_logs:
        if 'Booting paravirtualized kernel on bare hardware' in line:
            split_line = line.split()
            booting_log = split_line[0] + ' ' + split_line[1] + ' ' + split_line[2] + ' ' + split_line[7]
            booting_logs.append(booting_log)

    logs_batch = 60
    batch_items = booting_logs[:logs_batch]

    for item in batch_items:
        split_item = item.split()
        date = split_item[0] + ' ' + split_item[1]
        time = split_item[2]
        process = split_item[3]
    # Write date to sheets
        # Construct the row to be appended
        row = [date, time, process]
        # Determine the range to append the row
        table_range = 'A' + str(sheet.row_count + 1) + ':C' + str(sheet.row_count + 1)
        # Append the row to the sheet
        sheet.append_row(row, value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS', table_range=table_range)

def filter_sleep():
    print('This can take a minute, please dont exit the program.')
    sleep(60)
    for line in system_logs:
        if "Entering sleep state 'suspend'..." in line:
            split_line = line.split()
            sleep_log = split_line[0] + ' ' + split_line[1] + ' ' + split_line[2] + ' ' + split_line[5] + ' ' + split_line[6] + ' ' + split_line[7] + ' ' + split_line[8]
            sleep_logs.append(sleep_log)

    logs_batch = 60
    batch_items = sleep_logs[:logs_batch]
    for item in batch_items:
        split_item = item.split()
        date = split_item[0] + ' ' + split_item[1]
        time = split_item[2]
        process = split_item[4]
    # Write date to sheets
        # Construct the row to be appended
        row = [date, time, process]
        # Determine the range to append the row
        table_range = 'A' + str(sheet.row_count + 1) + ':C' + str(sheet.row_count + 1)
        # Append the row to the sheet
        sheet.append_row(row, value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS', table_range=table_range)

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]


# Load the credentials from the JSON key file and replace environment variables
credentials_dict = {
    "type": "service_account",
    "project_id": os.environ.get("PROJECT_ID"),
    "private_key_id": os.environ.get("PROJECT_KEY"),
    "private_key": os.environ.get("PRIVATE_KEY"),
    "client_email": os.environ.get("CLIENT_EMAIL"),
    "client_id": os.environ.get("CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get("CERT_URL"),
    "universe_domain": "googleapis.com"
}

# Load the credentials from the JSON key file
with open('syslogs-filter-key.json') as json_file:
    credentials_dict = json.load(json_file)

# Replace the placeholders in the credentials with environment variables
credentials_dict["project_id"] = os.environ.get("PROJECT_ID")
credentials_dict["private_key_id"] = os.environ.get("PROJECT_KEY")
credentials_dict["private_key"] = os.environ.get("PRIVATE_KEY")
credentials_dict["client_email"] = os.environ.get("CLIENT_EMAIL")
credentials_dict["client_id"] = os.environ.get("CLIENT_ID")
credentials_dict["client_x509_cert_url"] = os.environ.get("CERT_URL")

# Set the environment variables
os.environ["PROJECT_ID"] = credentials_dict["project_id"]
os.environ["PROJECT_KEY"] = credentials_dict["private_key_id"]
os.environ["PRIVATE_KEY"] = credentials_dict["private_key"]
os.environ["CLIENT_EMAIL"] = credentials_dict["client_email"]
os.environ["CLIENT_ID"] = credentials_dict["client_id"]
os.environ["CERT_URL"] = credentials_dict["client_x509_cert_url"]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scopes) #access the JSON key
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open("Ubuntu booting logs") #open sheet
sheet = sheet.worksheet('Logs') #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1


# Catch any error that might occur
try:
    with open(file_path) as file:
        file_content = file.read()
        for line in file_content.splitlines():
            system_logs.append(line)
except:
    print('Oops, wasnt able to open the file. Please review your code or the file.')

# Prompt the user for an option to filter for
print('Ubuntu syslog filter')
user_choice = input("Type 'sd' for shutdown filtering, 'b' for boot filtering, or 'sl' for sleep filtering: ")

if user_choice == 'sd':
    filter_shutdown()
elif user_choice == 'b':
    filter_boot()
elif user_choice == 'sl':
    filter_sleep()
else:
    print('Please select a valid option.')
    quit()