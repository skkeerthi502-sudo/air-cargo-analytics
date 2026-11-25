import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            print("MySQL Database Connected Successfully!")

        return connection

    except mysql.connector.Error as error:
        print("Database Connection Failed:", error)
        return None