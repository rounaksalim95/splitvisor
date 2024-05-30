# splitwiser

## Why?

I'm a huge fan of Splitwise and have been using it for a long time. However, recently they've made a change that completely put me off from using the app... They now only let you enter a certain number of expenses before blocking the user and asking them to update to a Pro account.

This completely destroyed my workflow as I would bulk add expenses in one shot once in a while as any good procrastinator would...

Fortunately, Splitwise has a pretty decent API that we can make use of instead. I ended up adding all my expenses to a Google Sheet and then just exported the data to a CSV that can be used to bulk add the expenses using the API.

This script will split the expenses equally among all members of the selected group.

## How to Use It

- Export all your expenses to a CSV file that looks something as follows:
```
Date,Expense,Total Amount,,
08/04/2023,Walmart,34.04,,
08/07/2023,Trader Joe's,50.5,,
08/12/2023,Safeway,10.99,,
```

- Generate an API key at https://secure.splitwise.com/oauth_clients

- Create a `.env` file with the following variables:
```
API_KEY=<your-api-key>
```

- Run `pip3 install -r requirements.txt` to install the dependencies

- Run `python3 splitwiser.py`

- Voila! The expenses will be added to the selected group and split equally!
