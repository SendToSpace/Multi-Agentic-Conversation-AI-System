import sqlite3

#TODO: MAKE SURE TO UPDATE DYNAMIC PATH FOR DATABASE IN PRODUCTION
# For now, we will use a static path for the database
db_path = "C:/Users/Jie/Desktop/Recipe/database/receipts.db"


conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS receipts ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    quantity INTEGER,
    unitPrice REAL,
    total Real,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')   

conn.commit()
conn.close()