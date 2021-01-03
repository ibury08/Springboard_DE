import mysql.connector
from mysql.connector import errorcode
import os
import csv


def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(user='root',
                                             password='my-secret-pw',
                                             host='db',
                                             port='3306',
                                             database='sales')
    except Exception as error:
        print("Error while connecting to database for job tracker", error)

    return connection


TABLES = {}

TABLES['ticket_sales'] = (
    "CREATE TABLE `ticket_sales` ("
    "`ticket_id` INT,"
    "`trans_date` DATE,"
    "`event_id` INT,"
    "`event_name` VARCHAR(50),"
    "`event_date` DATE,"
    "`event_type` VARCHAR(10),"
    "`event_city` VARCHAR(20),"
    #"`event_addr` VARCHAR(100),"
    "`customer_id` INT,"
    "`price` DECIMAL,"
    "`num_tickets` INT,"
    "PRIMARY KEY (`ticket_id`)"
    ") ENGINE=InnoDB"
)


def create_tables(connection, tables):
    cursor = connection.cursor()
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    cursor.close()


def load_third_pary(connection, file_path_csv):
    cursor = connection.cursor()

    with open(file_path_csv) as f:
        data = [tuple(line) for line in csv.reader(f)]

    add_ticket_sales = ("INSERT INTO ticket_sales "
                        "(ticket_id, trans_date, event_id, event_name, event_date, event_type,"
                        "event_city, customer_id, price, num_tickets)  VALUES"
                        "( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ")
    try:
        print(f"Inserting data: {len(data)} row(s).")
        cursor.executemany(add_ticket_sales, data)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print(f'OK: {cursor.rowcount} row(s) inserted.')

    connection.commit()
    cursor.close()


def query_popular_tickets(connection):
    sql_statement = "SELECT event_name, COUNT(num_tickets) as n_tickets FROM ticket_sales GROUP BY event_name ORDER BY n_tickets DESC LIMIT 3"
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    records = cursor.fetchall()
    cursor.close()
    return records


connection = get_db_connection()
create_tables(connection, TABLES['ticket_sales'])
load_third_pary(connection, './third_party_sales_1.csv')
events = query_popular_tickets(connection)
print('Here are the most popular tickets in the past month:')
for e in events:
    print(f'- {e[0]}')
connection.close()
