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
        print("STEP 0: DB connection acquired")

        try:
            print("STEP 1: idempotency check")
            existing = self.order_repo.find_by_order_id(conn, order_id)
            if existing:
                print("STEP 1A: existing order found")
                return {
                    "order_id": existing["order_id"],
                    "status": existing["status"]
                }

            print("STEP 2: domain validation")
            order = Order(order_id, user_id, amount)

            print("STEP 3: inserting order")
            self.order_repo.create(
                conn,
                order.order_id,
                order.user_id,
                order.amount,
                order.status
            )

            print("🔥 SIMULATING CRASH AFTER ORDER INSERT 🔥")
            raise RuntimeError("SIMULATED_CRASH_AFTER_ORDER_INSERT")

            print("STEP 4: inserting payment")  # never reached
            self.payment_repo.create(conn, order.order_id, "PAID")

            conn.commit()
            print("COMMIT SUCCESS")

            return {
                "order_id": order.order_id,
                "status": order.status
            }

        except Exception as e:
            print("ROLLBACK TRIGGERED DUE TO:", e)
            conn.rollback()
            raise

        finally:
            print("STEP FINAL: closing connection")
            conn.close()
