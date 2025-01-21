import argparse
import json
import os
from argparse import Namespace

expenses_file = "app.json"

def load_json():
    if not os.path.exists(expenses_file):
        return[]
    else:
        with open(expenses_file, 'r') as file:
            return json.load(file)

def save_to_json(expenses : list[dict]):
    with open(expenses_file, 'w') as file:
        json.dump(expenses, file, indent = 2)

def parser_handler():
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

def main():
    expenses: list[dict] = load_json()
    args : Namespace = parser_handler()
    save_to_json(expenses)