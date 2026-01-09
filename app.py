from flask import Flask, jsonify, request

from services.order_service import OrderService
from services.payment_service import PaymentService
from domain.errors import ValidationError, PaymentError

app = Flask(__name__)

# Initialize services (dependency injection)
payment_service = PaymentService()
order_service = OrderService(payment_service)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    for field in ["order_id", "user_id", "amount"]:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    order = order_service.place_order(
        data["order_id"],
        data["user_id"],
        data["amount"]
    )

    return jsonify({
        "order_id": order.order_id,
        "status": order.status
    }), 201
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"error": str(e)}), 400


@app.errorhandler(PaymentError)
def handle_payment_error(e):
    return jsonify({"error": str(e)}), 502


@app.errorhandler(Exception)
def handle_generic_error(e):
    return jsonify({"error": "Internal server error"}), 500
if __name__ == "__main__":
    app.run(debug=True)
