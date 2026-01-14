class PaymentRepository:

    def create(self, conn, order_id, status):
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO payments (order_id, status)
            VALUES (%s, %s)
            """,
            (order_id, status)
        )
        cursor.close()
