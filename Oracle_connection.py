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
    columns = [i[0] for i in cursor.description]
    return columns, result


def get_amount_by_kind():
    query = """select productKind, count(*)
       from campaign natural join product natural join promotes
       group by productKind
        order by count(*) DESC
            """
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    columns = [i[0] for i in cursor.description]
    return columns, result


def get_excelent_products():
    query = """SELECT productnumber, productname, productkind, count(*)
        From campaign natural join product natural join promotes
        where successrates > 9
        group by productnumber, productname, productkind
            """
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    columns = [i[0] for i in cursor.description]
    columns[3] = "amount of excellent campaigns"
    return columns, result


def best_campaigns():
    query = """select productkinD, avg(rating)
from tv_campaign natural join campaign natural join promotes natural join product
group by productkind
order by avg(rating - successrates) DESC
                """
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    columns = [i[0] for i in cursor.description]
    return columns, result


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

    # save json to file
    with open('static/data.json', 'w') as outfile:
        json.dump(json_data, outfile)

    return json_result
