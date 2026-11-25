from database.db_connection import get_connection

connection = get_connection()

if connection:
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM air_cargo_dataset")

    result = cursor.fetchone()

    print("Total Records:", result[0])

    cursor.close()
    connection.close()

    print("Database Connection Closed Successfully!")

else:
    print("Unable to Connect to MySQL Database.")