import mysql.connector
import os
from fastapi import Depends

def get_db_connection():
    # This function will be the dependency
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "parola1"),
            database=os.getenv("DB_NAME", "login_info")
        )
        return connection
    except mysql.connector.Error as err:
        print("Database Connection Error:", err)
        return None

def get_db():
    db = get_db_connection()
    try:
        yield db
    finally:
        if db:
            db.close() 