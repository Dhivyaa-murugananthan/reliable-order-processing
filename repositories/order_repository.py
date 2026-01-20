class OrderRepository:

    def find_by_order_id(self, conn, order_id):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT order_id, status FROM orders WHERE order_id = %s",
            (order_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        return row

    def create(self, conn, order_id, user_id, amount, status):
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO orders (order_id, user_id, amount, status)
            VALUES (%s, %s, %s, %s)
            """,
            (order_id, user_id, amount, status)
        )
        cursor.close()
