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
        print("STEP 0: DB connection acquired")
        conn = get_connection()

        try:
            # STEP 1: idempotency check
            print("STEP 1: idempotency check")
            existing = self.order_repo.find_by_order_id(conn, order_id)
            if existing:
                return {
                    "order_id": existing["order_id"],
                    "status": existing["status"]
                }

            # STEP 2: domain validation
            print("STEP 2: domain validation")
            order = Order(order_id, user_id, amount)

            # STEP 3: insert order
            print("STEP 3: inserting order")
            self.order_repo.create(
                conn,
                order.order_id,
                order.user_id,
                order.amount,
                order.status
            )

            # STEP 4: insert payment
            print("STEP 4: inserting payment")
            self.payment_repo.create(
                conn,
                order.order_id,
                "PAID"
            )

            # 💥 FAILURE SIMULATION POINT (AFTER PAYMENT)
            print("🔥 SIMULATING CRASH AFTER PAYMENT INSERT 🔥")
            raise RuntimeError("SIMULATED_CRASH_AFTER_PAYMENT_INSERT")

            # conn.commit()  ❌ NEVER REACHED

        except Exception as e:
            print("ROLLBACK TRIGGERED DUE TO:", e)
            conn.rollback()
            raise

        finally:
            print("STEP FINAL: closing connection")
            conn.close()
