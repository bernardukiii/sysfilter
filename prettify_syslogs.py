# Script to filter the information I want from syslog file
# I would like to retrieve the logs about system boot/reboot/turn off 
# Jun  4 21:38:15 mrrari14 systemd[973]: Reached target Shutdown.
# Jun 16 10:25:19 mrrari14 kernel: [    0.045535] Booting paravirtualized kernel on bare hardware
# Jun 16 12:02:58 mrrari14 systemd-sleep[25557]: Entering sleep state 'suspend'...
# Import libs to communicate with google api to access spreadsheets
import os
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
shutdown_logs = []
booting_logs = []
sleep_logs = []

# Function
def filter_shutdown():
    for line in file_content.splitlines():
        if 'Reached target Shutdown' in line:
            split_line = line.split()
            shutdown_log = split_line[0] + ' ' + split_line[1] + ' ' + split_line[2] + ' ' + split_line[7]
            shutdown_logs.append(shutdown_log)
            for item in shutdown_logs:
                print(item)

def filter_boot():
    for line in file_content.splitlines():
        if 'Booting paravirtualized kernel on bare hardware' in line:
            split_line = line.split()
            booting_log = split_line[0] + ' ' + split_line[1] + ' ' + split_line[2] + ' ' + split_line[7]
            booting_logs.append(booting_log)
            for item in booting_logs:
                print(item)

def filter_sleep():
    for line in file_content.splitlines():
        if "Entering sleep state 'suspend'..." in line:
            split_line = line.split()
            sleep_log = split_line[0] + ' ' + split_line[1] + ' ' + split_line[2] + ' ' + split_line[5] + ' ' + split_line[6] + ' ' + split_line[7] + ' ' + split_line[8]
            sleep_logs.append(sleep_log)
            for item in sleep_logs:
                print(item)

# Catch any error that might occur
try:
    with open(file_path) as file:
        file_content = file.read()
except:
    print('Oops, wasnt able to open the file. Please review your code or the file.')

# Prompt the user for an option to filter for
print('Ubuntu syslog filter')
# user_choice = input("Type 'sd' for shutdown filtering, 'b' for boot filtering, or 'sl' for sleep filtering: ")

# if user_choice == 'sd':
#     filter_shutdown()
# elif user_choice == 'b':
#     filter_boot()
# elif user_choice == 'sl':
#     filter_sleep()
# else: 
#     print('Please select a valid option.')
#     quit()

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
# cell_value = sheet.acell('A2')
# print(cell_value.value)