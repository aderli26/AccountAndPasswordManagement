import sqlite3
import settings

con = sqlite3.connect(settings.SQLITE_DB_PATH)

with open(settings.SQLITE_DB_SQL, mode='r') as f:
    con.cursor().executescript(f.read())
    
con.close()
print("Table created successfully")
