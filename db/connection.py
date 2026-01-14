import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="order_app",
        password="StrongAppPassword123",
        database="reliable_orders",
        autocommit=False
    )
