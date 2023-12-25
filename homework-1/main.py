"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import os
import csv
from dotenv import load_dotenv

load_dotenv()
postgres_key = os.getenv('POSTGRESSQL_KEY')

class RecieveDataFromCSV:
    @staticmethod
    def get_data_csv(filename):
        all_data = []
        with open(filename, encoding='utf-8') as file:
            full_data = csv.DictReader(file)
            for data in full_data:
                all_data.append(data)
        return all_data


data_reciever = RecieveDataFromCSV()

customers = data_reciever.get_data_csv('north_data/customers_data.csv')
employees = data_reciever.get_data_csv('north_data/employees_data.csv')

employee_id = 1
for employee in employees:
    employee['employee_id'] = employee_id
    employee_id += 1

orders = data_reciever.get_data_csv('north_data/orders_data.csv')

conn = psycopg2.connect(
    host='localhost',
    database='north',
    user='postgres',
    password=postgres_key
)

try:
    with conn:
        with conn.cursor() as cur:
            for customer in range(len(customers)):
                cur.execute(
                    'INSERT INTO customers VALUES (%s, %s, %s)',
                    (customers[customer]['customer_id'],
                     customers[customer]['company_name'],
                     customers[customer]['contact_name']))

            for employee in range(len(employees)):
                cur.execute(
                    'INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)',
                    (employees[employee]['employee_id'],
                     employees[employee]['first_name'],
                     employees[employee]['last_name'],
                     employees[employee]['title'],
                     employees[employee]['birth_date'],
                     employees[employee]['notes']))

            for order in range(len(orders)):
                cur.execute(
                    'INSERT INTO orders VALUES (%s, %s, %s, %s, %s)',
                    (orders[order]['order_id'],
                     orders[order]['customer_id'],
                     orders[order]['employee_id'],
                     orders[order]['order_date'],
                     orders[order]['ship_city']))
finally:
    conn.close()