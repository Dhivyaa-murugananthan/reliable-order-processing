# services/order_service.py
from domain.order import Order
from repositories.order_repository import OrderRepository
from repositories.payment_repository import PaymentRepository
from db.connection import get_connection


class OrderService:

    def __init__(self):
        self.order_repo = OrderRepository()
        self.payment_repo = PaymentRepository()

    def place_order(self, order_id, user_id, amount):
        conn = get_connection()

        try:
            # STEP 1: idempotency check
            existing = self.order_repo.find_by_order_id(conn, order_id)
            if existing:
                return {
                    "order_id": existing["order_id"],
                    "status": existing["status"]
                }

            # STEP 2: domain validation
            order = Order(order_id, user_id, amount)

            # STEP 3: create order
            self.order_repo.create(
                conn,
                order.order_id,
                order.user_id,
                order.amount,
                order.status
            )

            # STEP 4: create payment (DB enforces uniqueness)
            self.payment_repo.create(
                conn,
                order.order_id,
                "PAID"
            )

            conn.commit()

            return {
                "order_id": order.order_id,
                "status": order.status
            }

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()
