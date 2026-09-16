# Solution Rationale

## Product shape

FairPool is intentionally a small server-rendered Flask application. The core workflow is short: authenticate, create or reopen a pool, record contributions, inspect balances, and settle the remaining differences. Jinja templates keep the demo fast to run and easy to inspect, while vanilla JavaScript handles only dynamic participant and settlement-row interactions.

## Financial model

Money is represented as integer minor units rather than floating-point values. `calculate_fair_share()` distributes remainders deterministically, so the individual shares always add up to the target. Contributions are append-only records, which means a participant can pay multiple times without overwriting earlier payments.

Pool collection is deliberately separate from participant fairness. Collection answers whether the target has been funded; balances compare each participant with their fair share. This distinction also makes over-collection explicit: after participant debts are matched, remaining positive balances become pool refunds.

## Settlement

`generate_settlement()` uses deterministic greedy matching. Negative balances are debtors and positive balances are creditors. The algorithm matches the largest outstanding values first and emits only positive, non-self transfers. Organisers can save a custom plan, mark transfers settled, add rows, remove rows, or restore the generated suggestion. Custom plans do not rewrite contribution history.

## Persistence and UX

SQLite keeps the MVP self-contained and reliable for a demonstration. Pools, participants, contributions, and custom settlement plans persist across refreshes. The home page provides a history of created pools so the organiser can return to any dashboard instead of being forced into only the newest pool.

The interface uses a responsive server-rendered layout with a focused login screen, dashboard summary cards, mobile-friendly participant rows, and clear settlement/refund callouts. Authentication is intentionally a simple demo gate because the requested MVP excludes a full identity system.

## Validation

The financial module is isolated from Flask and database concerns, allowing focused tests for fair shares, balances, collection totals, settlement matching, and refunds. Flask test-client smoke checks cover login, pool creation, history, settlement editing, settled transfers, and over-collection display.