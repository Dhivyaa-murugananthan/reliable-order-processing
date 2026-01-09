from domain.errors import PaymentError


class PaymentService:
    def charge(self, user_id, amount):
        # simulate external dependency
        if amount > 10000:
            raise PaymentError("Payment gateway timed out")

        return {
            "status": "SUCCESS",
            "charged_amount": amount
        }
