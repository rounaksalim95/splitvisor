import os
from dotenv import load_dotenv
import requests
import csv
from datetime import datetime

# Splitwise API endpoint and access token
base_url = "https://secure.splitwise.com/api/v3.0"

load_dotenv()
access_token = os.getenv("API_KEY")

# Function to get user's groups


def get_groups():
    url = f"{base_url}/get_groups"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()["groups"]

# Function to create an expense


def create_expense(group_id, description, cost, date):
    url = f"{base_url}/create_expense"
    headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"}
    data = {
        "cost": str(cost),
        "description": description,
        "date": date.isoformat(),
        "group_id": group_id,
        "split_equally": True
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


# Get the path to the CSV or Excel file
file_path = input("Enter the path to the CSV or Excel file: ")

# Read the CSV or Excel file
expenses = []
with open(file_path, "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        date = datetime.strptime(row[0], "%Y-%m-%d")
        description = row[1]
        amount = float(row[2])
        expenses.append((date, description, amount))

# Get the user's groups
groups = get_groups()

# Display the groups and ask the user to select one
print("Select a group:")
for i, group in enumerate(groups):
    print(f"{i+1}. {group['name']}")
selected_group = int(input("Enter the number of the group: "))
group_id = groups[selected_group - 1]["id"]

# Create expenses in the selected group
for expense in expenses:
    date, description, amount = expense
    response = create_expense(group_id, description, amount, date)
    if "errors" in response:
        print(f"Error creating expense: {response['errors']}")
    else:
        print(f"Expense created: {response['expenses'][0]['description']}")
