import requests

url = "http://127.0.0.1:5000/orders"


payload = {
    "order_id": "ORD_FAIL_3",
    "user_id": 1,
    "amount": 500
}


r1 = requests.post(url, json=payload)
print("STATUS:", r1.status_code)
print("RAW RESPONSE:", repr(r1.text))

print("-" * 40)

r2 = requests.post(url, json=payload)
print("STATUS:", r2.status_code)
print("RAW RESPONSE:", repr(r2.text))
