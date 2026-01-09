class Order:
    CREATED = "CREATED"
    PAID = "PAID"
    FAILED = "FAILED"

    def __init__(self, order_id, user_id, amount):
        if not order_id:
            raise ValueError("order_id cannot be empty")
        if not user_id:
            raise ValueError("user_id cannot be empty")
        if amount <= 0:
            raise ValueError("amount must be greater than 0")

        self.order_id = order_id
        self.user_id = user_id
        self.amount = amount
        self.status = Order.CREATED

    def mark_paid(self):
        if self.status != Order.CREATED:
            raise ValueError("Only CREATED orders can be paid")
        self.status = Order.PAID

    def mark_failed(self):
        if self.status != Order.CREATED:
            raise ValueError("Only CREATED orders can fail")
        self.status = Order.FAILED
