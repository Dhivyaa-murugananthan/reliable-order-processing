# repositories/order_repository.py
import mysql.connector

class OrderRepository:

    def find_by_order_id(self, conn, order_id):
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT order_id, user_id, amount, status FROM orders WHERE order_id = %s",
                (order_id,)
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def create(self, conn, order_id, user_id, amount, status):
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO orders (order_id, user_id, amount, status)
                VALUES (%s, %s, %s, %s)
                """,
                (order_id, user_id, amount, status)
            )

        except mysql.connector.IntegrityError as e:
            # Duplicate order_id → someone else already inserted it
            if e.errno == 1062:
                # Swallow error, caller will re-fetch
                pass
            else:
                raise

        finally:
            cursor.close()
