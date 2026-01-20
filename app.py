from flask import Flask, request, jsonify
from services.order_service import OrderService
import services.order_service
print("ORDER_SERVICE LOADED FROM:", services.order_service.__file__)
app = Flask(__name__)

order_service = OrderService()


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    for field in ["order_id", "user_id", "amount"]:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        result = order_service.place_order(
            data["order_id"],
            data["user_id"],
            data["amount"]
        )
        return jsonify(result), 201
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

    """except Exception as e:
        print("UNEXPECTED ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500
"""

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
