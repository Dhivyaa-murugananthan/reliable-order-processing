import threading
import requests

URL = "http://127.0.0.1:5000/orders"

payload = {
    "order_id": "ORD_CONCURRENT_1",
    "user_id": 1,
    "amount": 999
}

def place_order(thread_id):
    try:
        r = requests.post(URL, json=payload)
        print(f"[Thread-{thread_id}] STATUS:", r.status_code, "RESPONSE:", r.text)
    except Exception as e:
        print(f"[Thread-{thread_id}] ERROR:", e)

threads = []

for i in range(5):  # 5 concurrent retries
    t = threading.Thread(target=place_order, args=(i,))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
