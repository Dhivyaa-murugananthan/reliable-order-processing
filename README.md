# Reliable Order Processing System

## Problem Statement
In real-world backend systems, clients may retry requests due to
network failures, timeouts, or lost responses. If order processing
is not designed carefully, retries can lead to duplicate orders
and double charges.

This project implements a backend system that safely processes
orders even under retries and partial failures.

---

## Core Guarantees
- Each `order_id` is processed at most once
- Payment is charged at most once per order
- Repeated requests return the same result
- System behavior is deterministic under retries

---

## Tech Stack
- Python
- Flask
- Git + GitHub

---

## Project Status
🚧 In progress
