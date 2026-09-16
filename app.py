import json
import os

from flask import Flask, flash, redirect, render_template, request, session, url_for

from models import Contribution, Participant, Pool, SettlementPlan, db
from settlement import calculate_balances, calculate_collection_status, calculate_fair_share, calculate_refunds, generate_settlement


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fairpool-demo-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///fairpool.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

DEMO_USERNAME = "admin"
DEMO_PASSWORD = "12345"


@app.before_request
def require_login():
    if request.endpoint in {"login", "static"}:
        return None
    if not session.get("authenticated"):
        return redirect(url_for("login", next=request.path))
    return None


def parse_amount(value):
    """Convert a user-facing amount into paise without floating-point arithmetic."""
    cleaned = value.strip().replace(",", "").replace("₹", "")
    if not cleaned or cleaned.startswith("-"):
        raise ValueError("Amount must be positive")
    whole, separator, fraction = cleaned.partition(".")
    if not whole.isdigit() or (separator and (not fraction.isdigit() or len(fraction) > 2)):
        raise ValueError("Enter a valid amount")
    return int(whole) * 100 + int((fraction + "00")[:2])


def format_money(amount, currency="INR"):
    symbols = {"INR": "₹", "USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, currency + " ")
    return f"{symbol}{amount // 100:,}.{amount % 100:02d}"


def pool_view_data(pool):
    ordered = sorted(pool.participants, key=lambda person: person.id)
    shares = calculate_fair_share(pool.target_amount, len(ordered))
    participant_inputs = []
    for participant in ordered:
        paid = sum(contribution.amount for contribution in participant.contributions)
        participant_inputs.append({"name": participant.name, "paid": paid})
    balances = calculate_balances(participant_inputs, shares)
    records = [{"participant": participant, **balance} for participant, balance in zip(ordered, balances)]
    collected = sum(item["paid"] for item in records)
    saved_plan = SettlementPlan.query.filter_by(pool_id=pool.id).first()
    settlement_adjustments = {participant.name: 0 for participant in ordered}
    if saved_plan:
        for transfer in json.loads(saved_plan.transfers):
            if transfer.get("settled"):
                settlement_amount = transfer.get("settled_amount", transfer["amount"])
                settlement_adjustments[transfer["from"]] += settlement_amount
                settlement_adjustments[transfer["to"]] -= settlement_amount
    for record in records:
        adjustment = settlement_adjustments[record["name"]]
        record["paid"] += adjustment
        record["balance"] += adjustment
    collection = calculate_collection_status(pool.target_amount, collected)
    collection["total_owed"] = sum(-item["balance"] for item in records if item["balance"] < 0)
    collection["total_overpaid"] = sum(item["balance"] for item in records if item["balance"] > 0)
    collection["people_owing"] = sum(item["balance"] < 0 for item in records)
    return records, collection, participant_inputs


def settlement_view_data(pool, records):
    generated = generate_settlement([{"name": item["participant"].name, "balance": item["balance"]} for item in records])
    saved_plan = SettlementPlan.query.filter_by(pool_id=pool.id).first()
    transfers = json.loads(saved_plan.transfers) if saved_plan else generated
    refunds = calculate_refunds([{"name": item["participant"].name, "balance": item["balance"]} for item in records], transfers)
    return transfers, refunds, bool(saved_plan)


@app.template_filter("money")
def money_filter(amount, currency="INR"):
    return format_money(amount, currency)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("authenticated"):
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            session["authenticated"] = True
            next_url = request.args.get("next") or url_for("index")
            safe_next_url = next_url if next_url.startswith("/") and not next_url.startswith("//") else url_for("index")
            return redirect(safe_next_url)
        flash("Incorrect username or password", "error")
    return render_template("login.html")


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    pools = Pool.query.order_by(Pool.created_at.desc()).all()
    return render_template("index.html", pools=pools)


@app.get("/new")
def new_pool():
    return redirect(url_for("index") + "#create-pool")


@app.post("/pools")
def create_pool():
    name = request.form.get("name", "").strip()
    participant_names = [name.strip() for name in request.form.getlist("participants") if name.strip()]
    try:
        target_amount = parse_amount(request.form.get("target_amount", ""))
        if not name or not participant_names or target_amount <= 0:
            raise ValueError("Add a pool name, target, and at least one participant")
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("index"))
    pool = Pool(name=name, target_amount=target_amount, currency=request.form.get("currency", "INR"))
    pool.participants = [Participant(name=person) for person in participant_names]
    db.session.add(pool)
    db.session.commit()
    return redirect(url_for("pool_dashboard", pool_id=pool.id))


@app.post("/demo")
def load_demo():
    pool = Pool(name="Manager Farewell Gift", target_amount=600000, currency="INR")
    names = ["Aman", "Riya", "Karan", "Neha", "Vivek", "Rahul"]
    pool.participants = [Participant(name=name) for name in names]
    db.session.add(pool)
    db.session.flush()
    payments = [100000, 70000, 0, 130000, 100000, 0]
    for participant, amount in zip(pool.participants, payments):
        if amount:
            db.session.add(Contribution(participant_id=participant.id, amount=amount))
    db.session.commit()
    return redirect(url_for("pool_dashboard", pool_id=pool.id))


@app.get("/pools/<int:pool_id>")
def pool_dashboard(pool_id):
    pool = Pool.query.get_or_404(pool_id)
    records, collection, _ = pool_view_data(pool)
    settlement_transfers, refunds, settlement_is_custom = settlement_view_data(pool, records)
    settlement_remaining = sum(item["amount"] for item in settlement_transfers if not item.get("settled"))
    settlement_settled = sum(bool(item.get("settled")) for item in settlement_transfers)
    return render_template("pool.html", pool=pool, records=records, collection=collection, refunds=refunds, settlement_transfers=settlement_transfers, settlement_is_custom=settlement_is_custom, settlement_remaining=settlement_remaining, settlement_settled=settlement_settled)


@app.post("/pools/<int:pool_id>/payments")
def add_payment(pool_id):
    pool = Pool.query.get_or_404(pool_id)
    try:
        participant = db.session.get(Participant, int(request.form.get("participant_id", "0")))
        amount = parse_amount(request.form.get("amount", ""))
        if not participant or participant.pool_id != pool.id or amount <= 0:
            raise ValueError("Choose a participant and enter a positive amount")
    except (ValueError, TypeError):
        flash("Choose a participant and enter a valid positive amount", "error")
        return redirect(url_for("pool_dashboard", pool_id=pool.id))
    db.session.add(Contribution(participant_id=participant.id, amount=amount))
    db.session.commit()
    flash(f"Payment recorded for {participant.name}", "success")
    return redirect(url_for("pool_dashboard", pool_id=pool.id))


@app.get("/pools/<int:pool_id>/settlement")
def settlement(pool_id):
    pool = Pool.query.get_or_404(pool_id)
    records, collection, _ = pool_view_data(pool)
    transfers, refunds, is_custom = settlement_view_data(pool, records)
    return render_template("settlement.html", pool=pool, collection=collection, transfers=transfers, refunds=refunds, participants=sorted(pool.participants, key=lambda person: person.id), is_custom=is_custom)


@app.post("/pools/<int:pool_id>/settlement")
def save_settlement(pool_id):
    pool = Pool.query.get_or_404(pool_id)
    participant_names = {participant.name for participant in pool.participants}
    from_names = request.form.getlist("transfer_from")
    to_names = request.form.getlist("transfer_to")
    amounts = request.form.getlist("transfer_amount")
    original_amounts = request.form.getlist("transfer_original_amount")
    settled_flags = request.form.getlist("transfer_settled")
    transfers = []
    try:
        for index, (payer, recipient, raw_amount) in enumerate(zip(from_names, to_names, amounts)):
            is_settled = str(index) in settled_flags
            parsed_amount = parse_amount(raw_amount)
            settlement_amount = parse_amount(original_amounts[index]) if is_settled and index < len(original_amounts) and original_amounts[index] else parsed_amount
            amount = 0 if is_settled else parsed_amount
            if payer not in participant_names or recipient not in participant_names or payer == recipient or (amount <= 0 and not is_settled):
                raise ValueError
            transfer = {"from": payer, "to": recipient, "amount": amount, "settled": is_settled}
            if is_settled:
                transfer["settled_amount"] = settlement_amount
            transfers.append(transfer)
    except ValueError:
        flash("Each settlement row needs two different participants and a positive amount", "error")
        return redirect(url_for("settlement", pool_id=pool.id))
    saved_plan = SettlementPlan.query.filter_by(pool_id=pool.id).first()
    if not saved_plan:
        saved_plan = SettlementPlan(pool_id=pool.id)
        db.session.add(saved_plan)
    saved_plan.transfers = json.dumps(transfers)
    db.session.commit()
    flash("Custom settlement plan saved", "success")
    return redirect(url_for("settlement", pool_id=pool.id))


@app.post("/pools/<int:pool_id>/settlement/reset")
def reset_settlement(pool_id):
    pool = Pool.query.get_or_404(pool_id)
    saved_plan = SettlementPlan.query.filter_by(pool_id=pool.id).first()
    if saved_plan:
        db.session.delete(saved_plan)
        db.session.commit()
    flash("Generated settlement plan restored", "success")
    return redirect(url_for("settlement", pool_id=pool.id))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)