import csv
import os
from typing import Final


LANGUAGES_CSV: Final = 'languages.csv'


def create_csv():
    with open(LANGUAGES_CSV, 'w', newline='') as csv_file:
        fieldnames = ['user_id', 'language']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()


def update_languages_list(data, user_id: int, language: str):
    for row in data:
        if int(row['user_id']) == user_id:
            row['language'] = language
            return data

    data.append({'user_id': str(user_id), 'language': language})
    return data


def update_user_preferred_language(user_id: int, language: str):
    data = read_data_from_csv()
    data = update_languages_list(data=data, user_id=user_id, language=language)
    write_data_to_csv(data)


def write_data_to_csv(data):
    with open(LANGUAGES_CSV, 'w', newline='') as csv_file:
        fieldnames = ['user_id', 'language']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)


def read_data_from_csv():
    with open(LANGUAGES_CSV, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)
    return data



