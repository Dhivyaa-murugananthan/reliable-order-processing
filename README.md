Reliable Order Processing System
Overview

This project implements a reliable, idempotent order processing system
designed to handle client retries, crashes, and partial failures
without causing duplicate orders or double charges.

The system is built to demonstrate real-world backend guarantees such as:

transactional consistency

idempotency under retries

safe failure handling with rollback verification

This is not a happy-path demo — failures are intentionally simulated
and verified at the database level.

Problem Statement

In real-world backend systems, clients may retry requests due to:

network timeouts

server restarts

load balancer retries

lost responses

If order processing is not carefully designed, retries can lead to:

duplicate orders

double payments

inconsistent system state

This project demonstrates how to design and verify a system that avoids
those failures.

Core Guarantees

The system enforces the following guarantees:

Each order_id is processed at most once

A payment is charged at most once per order

Repeated requests return the same result

No partial data is persisted on failure

Database state remains consistent under crashes

Design Decisions (Why This Works)
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

server restarts

multiple instances

crashes

Failure Simulation: Crash After Order Insert

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

Project Status

✅ Core functionality complete
🔬 Failure simulations implemented and verified
🧪 Additional failure scenarios planned

Why This Project Matters

This project demonstrates:

thinking in terms of system guarantees, not just endpoints

validating behavior under failure, not just success

using the database as a correctness boundary

communicating engineering decisions clearly