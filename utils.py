import csv
import os
import time
import requests
from requests.exceptions import ConnectTimeout


def get_request(url, parameters=None):
    try:
        response = requests.get(url=url, params=parameters)
        
    except ConnectTimeout as s:
        for i in range(5, 0, -1):
            print(f'Waiting... ({i})', end='\r')
            print(end='\x1b[2K')
            time.sleep(1)
        print('Retrying.' + ' '*10, end='\r')

        # Recusively try again
        return get_request(url, parameters)

    if response:
        return response.json()
    else:
        # Response is none usually means too many requests or reach limit. Wait and try again
        for i in range(10, 0, -1):
            print(f'Waiting... ({i})', end='\r')
            print(end='\x1b[2K')
            time.sleep(1)
        print('Retrying.' + ' '*10, end='\r')
        return get_request(url, parameters)


def prepare_csv(csv_filename, column):
    if not os.path.exists(csv_filename):
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=column)
            writer.writeheader()


def create_csv_from_dict(csv_filename, dict, column=None):
    if column is None:
        column = dict[0].keys()
    column = column
    prepare_csv(csv_filename, column)
    with open(csv_filename, 'a', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=column)
        writer.writerows(dict)


def create_csv(filename, arr):
    with open(filename, 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows([arr])


def create_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
