import argparse
import json
import os
from argparse import Namespace
from datetime import date
from tabulate import tabulate

expenses_file = "app.json"

def load_json():
    if not os.path.exists(expenses_file):
        with open(expenses_file, 'w') as file:
            file.write('[]')
    
    with open(expenses_file, 'r') as file:
        return json.load(file)

def save_to_json(expenses : list[dict]):
    with open(expenses_file, 'w') as file:
        json.dump(expenses, file, indent = 2)

def parser_handler() -> Namespace:
    parser = argparse.ArgumentParser(description = "CLI expense tracker")
    subparsers = parser.add_subparsers(dest = "command")

    add_parser = subparsers.add_parser('add', help = "add an expense")
    add_parser.add_argument('--description', type = str, help = "your expense description", required = True)
    add_parser.add_argument('--amount', type = int, help = "the amount you have spent", required = True)

    list_parser = subparsers.add_parser('list', help = "list all expenses")

    summary_parser = subparsers.add_parser('summary', help = "summary of all expenses")
    summary_parser.add_argument('--month', type = str, help = "the month of which the summary is needed")

    delete_parser = subparsers.add_parser('delete', help = "delete an expense")
    delete_parser.add_argument('--id', type = int, help = "id of the expense to delete", required = True)

    args = parser.parse_args()
    return args

def handle_command(args : Namespace, expenses : list[dict]):
    commands = {
        "add" : lambda : add_expense(args.description, args.amount, expenses),
        "list" :lambda : list_expenses(expenses) 
    }

    command = commands.get(args.command)
    if command:
        command()
    else:
        print("Invalid command")

def add_expense(desc : str, amount : int, expenses : list[dict]) -> None:
    if not expenses:
        expense_id = 1
    else:
        expense_id = max(expense['Id'] for expense in expenses) + 1

    new_expense = {
        "Id" : expense_id,
        "Date" : date.today().isoformat(),
        "Description" : desc,
        "Amount" : amount
    }

    expenses.append(new_expense)
    print("Expense added successfully")

def list_expenses(expenses : list[dict]) -> None:
    table = tabulate(expenses, headers = "keys")
    if table:
        print(table)
    else:
        print("No expenses to show")


def main():
    expenses = load_json()
    args : Namespace = parser_handler()
    handle_command(args, expenses)
    save_to_json(expenses)

if __name__ == "__main__":
    main()