# services/order_service.py
from domain.order import Order
from repositories.order_repository import OrderRepository
from repositories.payment_repository import PaymentRepository
from db.connection import get_connection


class OrderService:

    def __init__(self):
        self.order_repo = OrderRepository()
        self.payment_repo = PaymentRepository()

# services/order_service.py

    def place_order(self, order_id, user_id, amount):
        conn = get_connection()

        try:
            print("STEP 0: DB connection acquired")

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

            # STEP 5: COMMIT
            print("STEP 5: committing transaction")
            conn.commit()

            # 🚨 STEP 6: crash AFTER commit
            print("🔥 SIMULATING CRASH AFTER COMMIT 🔥")
            raise RuntimeError("SIMULATED_POST_COMMIT_CRASH")

            # unreachable
            return {
                "order_id": order.order_id,
                "status": order.status
            }

        except Exception as e:
            print("ERROR OCCURRED:", e)
            raise

        finally:
            print("STEP FINAL: closing connection")
            conn.close()
