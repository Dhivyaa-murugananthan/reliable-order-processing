# services/order_service.py

from domain.order import Order
from repositories.order_repository import OrderRepository
from repositories.payment_repository import PaymentRepository
from db.connection import get_connection
import mysql.connector


class OrderService:

    def __init__(self):
        self.order_repo = OrderRepository()
        self.payment_repo = PaymentRepository()

    def place_order(self, order_id, user_id, amount):
        conn = get_connection()

        try:
            print("STEP 0: DB connection acquired")

            # STEP 1: Idempotency check (fast path)
            print("STEP 1: idempotency check")
            existing = self.order_repo.find_by_order_id(conn, order_id)
            if existing:
                print("ORDER ALREADY EXISTS → returning existing result")
                return {
                    "order_id": existing["order_id"],
                    "status": existing["status"]
                }

            # STEP 2: Domain validation
            print("STEP 2: domain validation")
            order = Order(order_id, user_id, amount)

            # STEP 3: Insert order
            print("STEP 3: inserting order")
            self.order_repo.create(
                conn,
                order.order_id,
                order.user_id,
                order.amount,
                order.status
            )

            # STEP 4: Insert payment (protected by UNIQUE constraint)
            print("STEP 4: inserting payment")
            self.payment_repo.create(
                conn,
                order.order_id,
                "PAID"
            )

            conn.commit()
            print("STEP 5: transaction committed")

            return {
                "order_id": order.order_id,
                "status": order.status
            }

        # ✅ IMPORTANT: handle payment uniqueness violation FIRST
        except mysql.connector.errors.IntegrityError as e:
            print("INTEGRITY ERROR:", e)
            conn.rollback()

            # Concurrent retry: payment already created by another request
            if "uq_payment_order" in str(e):
                print("CONCURRENT PAYMENT DETECTED → returning canonical order")

                existing = self.order_repo.find_by_order_id(conn, order_id)
                return {
                    "order_id": existing["order_id"],
                    "status": existing["status"]
                }

            # Any other integrity error is real
            raise

        # Generic safety net
        except Exception as e:
            print("UNEXPECTED ERROR:", e)
            conn.rollback()
            raise

        finally:
            print("STEP FINAL: closing DB connection")
            conn.close()
