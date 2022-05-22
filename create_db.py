import psycopg2

connection=psycopg2.connect(
        host="127.0.0.1",
        user="postgres",
        password="postgres",
        database="postgres"
        )
connection.autocommit=True
with connection.cursor() as cursor:
        cursor.execute(
            "CREATE DATABASE fstek;"
        )
        
        print("[INFO] DATDABASE create successfully!") 