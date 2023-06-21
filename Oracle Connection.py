from datetime import datetime

import cx_Oracle
import json

connection = cx_Oracle.connect(
    user="sys",
    password="password",
    mode=cx_Oracle.SYSDBA)

cursor = connection.cursor()

# define columns
campaign_columns = ["start date", "end date", "success rates", "campaign id", "agency name", "presenter id"]
presenter_columns = ["name", "seniority", "phone", "presenter id"]
product_columns = ["product name", "product number", "product kind"]


# define functions that will return tables in json format

def get_campaigns():
    cursor.execute("SELECT * FROM campaign")
    result = cursor.fetchall()
    return campaign_columns, result


def get_presenters():
    cursor.execute("SELECT * FROM presenter")
    result = cursor.fetchall()
    return presenter_columns, result


def get_products():
    cursor.execute("SELECT * FROM product")
    result = cursor.fetchall()
    return product_columns, result


def apply_query(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result


import json
from datetime import datetime

def convert_to_json(column_names, result):
    # Create an empty list to store the row data
    json_data = []

    for row in result:
        data = {}
        for i, column in enumerate(row):
            # Check if column is a datetime object
            if isinstance(column, datetime):
                # Convert datetime object to yyyy-mm-dd  format
                column = column.strftime("%Y-%m-%d")
            # Add column value to the data dictionary
            data[column_names[i]] = column

        # Add the data dictionary to the JSON list
        json_data.append(data)

    # Serialize the JSON list
    json_result = json.dumps(json_data)

    return json_result


print(convert_to_json(*get_campaigns()))

