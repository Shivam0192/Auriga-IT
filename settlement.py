"""Pure financial calculations for FairPool.

All amounts are integer minor units (paise for INR). Keeping this module free
of Flask and database dependencies makes the money rules easy to test.
"""


def calculate_fair_share(target_amount, participant_count):
    """Allocate a target exactly across participants, giving early people the remainder."""
    if participant_count <= 0:
        return []
    base, remainder = divmod(target_amount, participant_count)
    return [base + (1 if index < remainder else 0) for index in range(participant_count)]


def calculate_balances(participants, fair_shares=None):
    """Return paid, fair share, and balance records for participant dictionaries."""
    if fair_shares is None:
        fair_shares = calculate_fair_share(sum(item.get("fair_share", 0) for item in participants), len(participants))
    balances = []
    for index, participant in enumerate(participants):
        fair_share = fair_shares[index]
        paid = participant.get("paid", 0)
        balances.append({
            "name": participant["name"],
            "fair_share": fair_share,
            "paid": paid,
            "balance": paid - fair_share,
        })
    return balances


def calculate_collection_status(target_amount, collected):
    """Describe pool funding independently from individual contribution fairness."""
    remaining = max(target_amount - collected, 0)
    percentage = (collected / target_amount * 100) if target_amount else 0
    return {
        "target": target_amount,
        "collected": collected,
        "remaining": remaining,
        "percentage": min(percentage, 100),
        "is_funded": collected >= target_amount,
        "overage": max(collected - target_amount, 0),
    }


def generate_settlement(balances):
    """Greedily match debtors and creditors with the fewest practical transfers."""
    debtors = [[item["name"], -item["balance"]] for item in balances if item["balance"] < 0]
    creditors = [[item["name"], item["balance"]] for item in balances if item["balance"] > 0]
    debtors.sort(key=lambda item: (-item[1], item[0]))
    creditors.sort(key=lambda item: (-item[1], item[0]))

    transfers = []
    debtor_index = creditor_index = 0
    while debtor_index < len(debtors) and creditor_index < len(creditors):
        debtor, owed = debtors[debtor_index]
        creditor, due = creditors[creditor_index]
        amount = min(owed, due)
        if amount > 0 and debtor != creditor:
            transfers.append({"from": debtor, "to": creditor, "amount": amount})
        debtors[debtor_index][1] -= amount
        creditors[creditor_index][1] -= amount
        if debtors[debtor_index][1] == 0:
            debtor_index += 1
        if creditors[creditor_index][1] == 0:
            creditor_index += 1
    return transfers


def calculate_refunds(balances, transfers):
    """Return remaining positive balances as refunds from an over-collected pool."""
    remaining = {item["name"]: item["balance"] for item in balances if item["balance"] > 0}
    for transfer in transfers:
        if transfer.get("settled"):
            continue
        if transfer["to"] in remaining:
            remaining[transfer["to"]] = max(remaining[transfer["to"]] - transfer["amount"], 0)
    return [{"name": name, "amount": amount} for name, amount in remaining.items() if amount > 0]