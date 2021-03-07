import sqlite3
import pandas as pd

con = sqlite3.connect("db.sqlite3")
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
cursor.close()
con.close()


def to_csv():
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * from %s" % table_name, db)
        
        table.to_csv(table_name + ".csv", index_label="index")
    cursor.close()
    db.close()


to_csv()