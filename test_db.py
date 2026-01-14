from db.connection import get_connection

conn = get_connection()
print("Connected:", conn.is_connected())
conn.close()
