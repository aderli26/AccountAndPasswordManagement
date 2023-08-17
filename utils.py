
import sqlite3

def connect_DB(db):
    con = sqlite3.connect(db)
    
    return con

def http_response(success,reason):
    return {"success":success,"reason":reason}