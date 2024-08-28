import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime

def get_data_type(value):
    if isinstance(value, int):
        return 'INT'
    elif isinstance(value, float):
        return 'DECIMAL(18, 10)'  # Adjust decimal precision if needed
    elif isinstance(value, str):
        return 'VARCHAR(255)'  
    else:
        return 'VARCHAR(255)' 

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

host = 'localhost'
user = 'root'
password = ''
database = 'metals_prices'
table_name = 'metals_rates'
json_file_path = './api_data.json'

with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

flat_json_data = flatten_dict(json_data)

try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Create table query with modifications
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ("
        create_table_query += "`id` INT AUTO_INCREMENT PRIMARY KEY, "
        create_table_query += "`date` DATETIME, "  # Adding date column
        for key, value in flat_json_data.items():
            if key != 'success' and key != 'timestamp':  
                # Remove 'rates_' prefix from column names
                column_name = key.replace('rates_', '')
                create_table_query += f"`{column_name}` {get_data_type(value)}, "
        create_table_query = create_table_query.rstrip(', ') + ")"

        print(f"SQL Query: {create_table_query}")
        cursor.execute(create_table_query)

        # Prepare insert query
        insert_query = f"INSERT INTO `{table_name}` ("
        insert_query += '`date`, '  # Include date column
        insert_query += ', '.join(key.replace('rates_', '') for key in flat_json_data if key != 'success' and key!= 'timestamp')
        insert_query += f") VALUES (%s, "  # Include date placeholder
        insert_query += ', '.join(['%s'] * (len(flat_json_data) - 2))  # Adjust placeholders
        insert_query += ")"

        # Prepare values
        values = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),)  # Current date
        values += tuple(flat_json_data[key] if not isinstance(flat_json_data[key], list) else json.dumps(flat_json_data[key]) for key in flat_json_data if key != 'success' and key!='timestamp')

        cursor.execute(insert_query, values)
        connection.commit()

        print("Data inserted successfully")

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
