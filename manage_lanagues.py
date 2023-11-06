import csv
import os
from typing import Final


LANGUAGES_CSV: Final = 'languages.csv'


def create_csv():
    with open(LANGUAGES_CSV, 'w', newline='') as csv_file:
        fieldnames = ['user_id', 'language']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()


def update_data(data, user_id: int, language: str):
    # Find the matching row and update it if user_id exists
    user_id_exists = False
    for row in data:
        if int(row['user_id']) == user_id:
            row['language'] = language
            user_id_exists = True
            break

    # If user_id doesn't exist, add a new row
    if not user_id_exists:
        data.append({'user_id': str(user_id), 'language': language})

    return data


def update_csv(user_id: int, language: str):
    # Open the CSV file for reading and create a list of dictionaries from its contents
    with open(LANGUAGES_CSV, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)

    data = update_data(data=data, user_id=user_id, language=language)

    # Write the updated data back to the CSV file
    with open(LANGUAGES_CSV, 'w', newline='') as csv_file:
        fieldnames = ['user_id', 'language']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)


def matching_language(user_id:int):
    # Read the CSV file and search for the user_id
    with open(LANGUAGES_CSV, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if int(row['user_id']) == user_id:
                return


