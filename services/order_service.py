from domain.order import Order
from domain.errors import ValidationError, PaymentError


class OrderService:
    def __init__(self, payment_service):
        self.payment_service = payment_service
        self._orders = {}  # order_id -> Order

    def place_order(self, order_id, user_id, amount):
        # idempotency check
        if order_id in self._orders:
            return self._orders[order_id]

        # create domain object
        order = Order(order_id, user_id, amount)

        try:
            payment_result = self.payment_service.charge(
                order.user_id, order.amount
            )
            order.mark_paid()
        except PaymentError:
            order.mark_failed()
            raise

        self._orders[order_id] = order
        return order
