import requests

url = "http://127.0.0.1:5000/orders"

payload = {
    "order_id": "ORD1",
    "user_id": "U1",
    "amount": 500
}

r1 = requests.post(url, json=payload)
r2 = requests.post(url, json=payload)

print(r1.status_code, r1.json())
print(r2.status_code, r2.json())
