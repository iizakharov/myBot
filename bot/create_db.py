import sqlite3
import datetime
from tabulate import tabulate

conn = sqlite3.connect("my_DB.db", check_same_thread=False)
cursor = conn.cursor()
date = datetime.datetime.today()
month = date.strftime('%B %Y')


# Создание таблицы
def create_table(table):
    cursor.execute(f"""CREATE TABLE {table}
                   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   summ INTEGER NOT NULL, in_date TEXT NOT NULL)""")


# DELETE TABLE
def drop_table(table):
    cursor.execute(f"""DROP TABLE {table}""")


def i_got(table):
    statement = f"select sum(summ) from {table}"
    cursor.execute(statement)
    result = cursor.fetchone()[0]
    return result


def add_summ(summ, table):
    date = datetime.datetime.today()
    month = date.strftime('%B')
    # Вставляем данные в таблицу
    cursor.execute(f"INSERT INTO {table}(summ, in_date) \
                      VALUES ('{int(summ)}', '{date.strftime('%d-%m-%Y')}')"
                   )
    conn.commit()


def count(table):
    statement = f"select count(summ) from {table}"
    cursor.execute(statement)
    result = cursor.fetchone()[0]
    return result


def get_all(table):
    statement = f"select * from {table}"
    cursor.execute(statement)
    author_tuples = cursor.fetchall()
    result = []
    headers = ["Номер", "Сумма", "Дата"]
    for i in author_tuples:
        result.append(i)
    return tabulate(result, headers)


def delete(table, id):
    sql = f"DELETE FROM {table} WHERE id=?"
    cursor.execute(sql, (id,))
    conn.commit()
