class OrderRepository:

    def find_by_order_id(self, conn, order_id):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT order_id, user_id, amount, status
            FROM orders
            WHERE order_id = %s
            """,
            (order_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        return row
