import os
from dotenv import load_dotenv
import requests
import csv
from datetime import datetime

# Splitwise API endpoint
base_url = "https://secure.splitwise.com/api/v3.0"

load_dotenv()
access_token = os.getenv("API_KEY")


def get_groups():
    """
    Fetches the groups from the Splitwise API.

    Returns:
        A list of groups available under the authenticated user's account.
    """
    url = f"{base_url}/get_groups"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()["groups"]


def create_expense(group_id, description, cost, date):
    """
    Creates an expense in a specified group on Splitwise.

    Args:
        group_id (int): The ID of the group where the expense will be created.
        description (str): A description of the expense.
        cost (float): The total cost of the expense.
        date (datetime): The date when the expense occurred.

    Returns:
        A JSON response from the Splitwise API after attempting to create the expense.
    """
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
    """
    Reads expenses from a CSV file and stores them in a list.

    The CSV file should have the following columns: Date, Description, Amount.
    The Date should be in MM/DD/YYYY format.
    """
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        date = datetime.strptime(row[0], "%m/%d/%Y")
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
    """
    Iterates through the list of expenses, creating each one in the selected Splitwise group.
    """
    date, description, amount = expense
    response = create_expense(group_id, description, amount, date)
    if response["errors"]:
        print(f"Error creating expense: {response['errors']}")
    else:
        print(f"Expense created for {response['expenses'][0]['description']} with total cost of ${response['expenses'][0]['cost']}")
