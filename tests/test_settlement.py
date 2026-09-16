from settlement import calculate_balances, calculate_collection_status, calculate_fair_share, calculate_refunds, generate_settlement
from import_data import import_contributions


def test_fair_share_allocates_remainder_without_losing_money():
    shares = calculate_fair_share(100, 3)
    assert shares == [34, 33, 33]
    assert sum(shares) == 100


def test_balances_and_collection_status():
    balances = calculate_balances([{"name": "Aman", "paid": 1000}, {"name": "Riya", "paid": 700}], [1000, 1000])
    assert [item["balance"] for item in balances] == [0, -300]
    status = calculate_collection_status(2000, 1700)
    assert status["remaining"] == 300
    assert status["collected"] == 1700


def test_overpayment_is_positive_balance():
    balances = calculate_balances([{"name": "Neha", "paid": 1300}], [1000])
    assert balances[0]["balance"] == 300


def test_settlement_is_deterministic_and_exact():
    transfers = generate_settlement([
        {"name": "Riya", "balance": -300},
        {"name": "Karan", "balance": -1000},
        {"name": "Neha", "balance": 300},
        {"name": "Vivek", "balance": 1000},
    ])
    assert transfers == [
        {"from": "Karan", "to": "Vivek", "amount": 1000},
        {"from": "Riya", "to": "Neha", "amount": 300},
    ]


def test_over_collection_becomes_refund_after_settlement():
    balances = [
        {"name": "Asha", "balance": -100},
        {"name": "Dev", "balance": 300},
    ]
    transfers = [{"from": "Asha", "to": "Dev", "amount": 100}]
    assert calculate_refunds(balances, transfers) == [{"name": "Dev", "amount": 200}]


def test_messy_import_merges_duplicates_and_rejects_invalid_rows():
    text = 'name,amount\nAman,"₹1,000"\nAMAN,1000\nRiya, 700 \nRia,"₹700"\nKaran,not-money\n,500\n'
    accepted, report = import_contributions(text, ["Aman", "Riya"])
    assert len(accepted) == 2
    assert report["imported"] == 2
    assert len(report["duplicates"]) == 2
    assert len(report["merged"]) == 2
    assert len(report["rejected"]) == 2