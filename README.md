**Reliable Order Processing System**
**Overview**

This project implements a reliable, idempotent order processing system
designed to handle client retries, crashes, and partial failures
without causing duplicate orders or double charges.

The system is built to demonstrate real-world backend guarantees such as:

* transactional consistency

* idempotency under retries

* safe failure handling with rollback verification

This is not a happy-path demo — failures are intentionally simulated
and verified at the database level.

**Problem Statement**

In real-world backend systems, clients may retry requests due to:

* network timeouts

* server restarts

* load balancer retries

* lost responses

If order processing is not carefully designed, retries can lead to:

* duplicate orders

* double payments

* inconsistent system state

This project demonstrates how to design and verify a system that avoids
those failures.

**Core Guarantees**

The system enforces the following guarantees:

* Each order_id is processed at most once

* A payment is charged at most once per order

* Repeated requests return the same result

* No partial data is persisted on failure

* Database state remains consistent under crashes

**Design Decisions** (Why This Works)
1. Database-backed Idempotency

order_id is treated as a business-level idempotency key

Payments table enforces a UNIQUE constraint on order_id

Duplicate requests are rejected at the database level, not just in Python

2. Transactional Order + Payment Flow

Order creation and payment insertion run inside one DB transaction

If any step fails, the entire transaction is rolled back

Prevents partial writes and inconsistent state

3. No In-Memory State

No in-memory caches or dictionaries are used for correctness

System remains safe across:

* server restarts

* multiple instances

* crashes

Failure Simulation 1: Crash After Order Insert

To prove transactional safety, the system intentionally simulates a crash
after inserting the order but before inserting the payment.

Simulated Failure
🔥 SIMULATING CRASH AFTER ORDER INSERT 🔥
ROLLBACK TRIGGERED DUE TO: SIMULATED_CRASH_AFTER_ORDER_INSERT

HTTP Response
{
  "error": "Internal server error"
}

Database Verification

After the crash, the database was queried manually:

SELECT * FROM orders WHERE order_id = 'ORD_FAIL_1';
SELECT * FROM payments WHERE order_id = 'ORD_FAIL_1';


Result:

Empty set


✔ Confirms that the transaction was fully rolled back
✔ No partial order or payment was persisted

Tech Stack

Python

Flask

MySQL

Git + GitHub

Git History & Experiment Tracking

Failure simulations and experiments are committed separately
to preserve a clean and understandable history.

Example:

feat: simulate crash after order insert and verify transaction rollback

main branch contains stable, production-ready behavior

This mirrors real-world engineering workflows where experiments
are isolated and traceable.


---

## Failure Simulation 2 – Crash After Payment Insert

### Scenario
This simulation tests a critical failure case where the system crashes **after inserting the payment record but before committing the transaction**.

This mirrors real-world failures such as:
- Application crash after charging a payment
- Process kill or container restart
- Unexpected runtime exception

---

### Steps Simulated
1. Start database transaction
2. Insert order record into `orders` table
3. Insert payment record into `payments` table
4. **Simulate a crash immediately after payment insert**
5. Trigger transaction rollback

---

### Expected Behavior
- ❌ Order **must not** exist in the database
- ❌ Payment **must not** exist in the database
- ✅ Client receives `500 Internal Server Error`
- ✅ Retrying the same request is safe (no double charge)

---

### Verification

#### HTTP Response Key Takeaways
```json
{
  "error": "Internal server error"
}
Database Validation
sql

SELECT * FROM orders WHERE order_id = 'ORD_FAIL_2';
-- Empty set

SELECT * FROM payments WHERE order_id = 'ORD_FAIL_2';
-- Empty set
Both tables remain unchanged, confirming atomic rollback across multiple writes.

---

#### Key Takeaways
Transactions protect against partial writes

Database-level atomicity is stronger than application-level checks

System remains safe under retries and crashes

This simulation proves that even the worst-case failure does not cause data corruption or double charging.

---
📌 Project Status
✅ Completed Core Features

* Idempotent order creation using order_id

* Database-backed transaction management

* Safe retry handling without duplicate orders or payments

* Strong consistency guarantees using MySQL constraints

✅ Failure Scenarios Verified

* Crash after order insert → full rollback

* Crash after payment insert → full rollback

* No partial writes persisted in any failure case

* Client receives safe 500 response and can retry

✅ Data Integrity Guarantees

* order_id enforced as unique

* payments.order_id protected by a unique constraint

* Foreign key enforcement between orders and payments

* Atomic commit / rollback across multiple tables

🧪 Test Coverage

* Manual API tests using Python client

* SQL verification after simulated crashes

* Explicit rollback validation using database queries

🚀 Current State

* Production-grade core logic complete.
* System is resilient to retries, crashes, and partial execution.

🔜 Optional Next Enhancements

* Retry-safe API responses after post-commit crashes

* Background processing / outbox pattern

* Async payment handling

* Structured logging & monitoring

