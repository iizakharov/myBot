import sqlite3
import datetime
import logging
from tabulate import tabulate
from decos import log

conn = sqlite3.connect("my_DB.db", check_same_thread=False)
cursor = conn.cursor()
date = datetime.datetime.today()
month = date.strftime('%B %Y')


# Создание таблицы
@log
def create_table(table):
    cursor.execute(f"""CREATE TABLE {table}
                   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   summ INTEGER NOT NULL, in_date TEXT NOT NULL)""")


# DELETE TABLE
@log
def drop_table(table):
    cursor.execute(f"""DROP TABLE {table}""")

@log
def i_got(table):
    statement = f"select sum(summ) from {table}"
    cursor.execute(statement)
    result = cursor.fetchone()[0]
    return result

@log
def add_summ(summ, table):
    date = datetime.datetime.today()
    month = date.strftime('%B')
    # Вставляем данные в таблицу
    cursor.execute(f"INSERT INTO {table}(summ, in_date) \
                      VALUES ('{int(summ)}', '{date.strftime('%d-%m-%Y')}')"
                   )
    conn.commit()

@log
def count(table):
    statement = f"select count(summ) from {table}"
    cursor.execute(statement)
    result = cursor.fetchone()[0]
    return result

@log
def get_all(table):
    statement = f"select * from {table}"
    cursor.execute(statement)
    author_tuples = cursor.fetchall()
    result = []
    headers = ["Номер", "Сумма", "Дата"]
    for i in author_tuples:
        result.append(i)
    return tabulate(result, headers)


@log
def get_month(table):
    statement = f"select * from {table}"
    cursor.execute(statement)
    author_tuples = cursor.fetchall()
    result = []
    headers = ["Номер", "Сумма", "Дата"]
    for i in author_tuples:
        result.append(i)
    return tabulate(result, headers)


@log
def delete(table, id):
    sql = f"DELETE FROM {table} WHERE id=?"
    cursor.execute(sql, (id,))
    conn.commit()

