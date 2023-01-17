import sqlite3

conn = sqlite3.connect('ahun.sqlite')
cursor = conn.cursor()

word = (str(input("What is the word?")), )
cursor.execute("SELECT AMH FROM dictionary WHERE _id=?", word)
result = cursor.fetchall()

print(result)
