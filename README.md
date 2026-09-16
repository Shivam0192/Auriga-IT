# FairPool

FairPool is a Flask and SQLite application for tracking group contributions, participant balances, settlement transfers, and refunds from over-collected pools.

## Requirements

- Python 3.11 or newer
- `pip`

## Setup

```bash
python3 -m pip install -r requirements.txt
```

## Run

```bash
python3 app.py
```

Open http://127.0.0.1:5000 in a browser.

The demo login is:

- Username: `admin`
- Password: `12345`

Use **Load demo** to create a sample pool with paid, partially paid, unpaid, and overpaid participants.

## Test

```bash
pytest -q
python3 -m py_compile app.py models.py settlement.py
```

The tests focus on integer paise calculations, uneven fair-share allocation, collection status, overpayment, settlement generation, and over-collection refunds.

## Database

The default database is SQLite at `instance/fairpool.db`. SQLAlchemy creates the tables on application startup. To use another database URL:

```bash
DATABASE_URL=sqlite:////tmp/fairpool.db python3 app.py
```

Core tables are `Pool`, `Participant`, `Contribution`, and the persisted custom `SettlementPlan`.

## Debugging

Run Flask in debug mode with:

```bash
FLASK_DEBUG=1 python3 app.py
```

For a clean local database, stop the server and remove `instance/fairpool.db`, then start the application again. Do not remove the database if you need to preserve pool history and payments.

Useful checks:

```bash
git status --short
pytest -q
curl -I http://127.0.0.1:5000/login
```

All money values are stored as integer minor units. For INR, ₹100.50 is stored as `10050` paise, preventing floating-point rounding errors.