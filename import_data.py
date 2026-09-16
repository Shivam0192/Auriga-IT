import csv
import io
import re
from difflib import SequenceMatcher


def normalize_name(value):
    """Create a comparison key for names while retaining the first clean display name."""
    return re.sub(r"[^a-z0-9]", "", value.strip().casefold())


def parse_import_amount(value):
    """Parse common currency formats into integer minor units."""
    cleaned = str(value or "").strip().replace("₹", "").replace("$", "").replace("€", "")
    cleaned = cleaned.replace("INR", "").replace("USD", "").replace("EUR", "").replace(",", "").strip()
    if not cleaned or cleaned.startswith("-") or not re.fullmatch(r"\d+(?:\.\d{1,2})?", cleaned):
        raise ValueError("invalid amount")
    whole, _, fraction = cleaned.partition(".")
    return int(whole) * 100 + int((fraction + "00")[:2])


def resolve_name(raw_name, known_names):
    """Match case/spacing variants and conservative close spellings to one display name."""
    clean_name = re.sub(r"\s+", " ", raw_name.strip())
    key = normalize_name(clean_name)
    if not key:
        raise ValueError("missing name")
    for known_name in known_names:
        known_key = normalize_name(known_name)
        if key == known_key or SequenceMatcher(None, key, known_key).ratio() >= 0.84:
            return known_name, False
    return clean_name, True


def import_contributions(text, known_names):
    """Clean CSV text and return accepted rows plus an auditable import report."""
    reader = csv.DictReader(io.StringIO(text.lstrip("\ufeff")))
    if not reader.fieldnames:
        raise ValueError("CSV must include a header row")
    fields = {re.sub(r"[^a-z]", "", field.casefold()): field for field in reader.fieldnames if field}
    name_field = next((fields[key] for key in ("name", "person", "participant", "participantname") if key in fields), None)
    amount_field = next((fields[key] for key in ("amount", "paid", "payment", "contribution") if key in fields), None)
    if not name_field or not amount_field:
        raise ValueError("CSV needs a name/person and amount/paid column")

    names = list(known_names)
    accepted = []
    rejected = []
    duplicates = []
    merged = []
    seen_rows = set()
    for row_number, row in enumerate(reader, start=2):
        raw_name = row.get(name_field, "")
        raw_amount = row.get(amount_field, "")
        try:
            resolved_name, is_new = resolve_name(raw_name, names)
            amount = parse_import_amount(raw_amount)
            if amount <= 0:
                raise ValueError("amount must be positive")
        except ValueError as error:
            rejected.append({"row": row_number, "reason": str(error), "raw": f"{raw_name} / {raw_amount}"})
            continue
        if not is_new and raw_name.strip() != resolved_name:
            merged.append({"row": row_number, "from": raw_name.strip(), "to": resolved_name})
        duplicate_key = (normalize_name(resolved_name), amount)
        if duplicate_key in seen_rows:
            duplicates.append({"row": row_number, "name": resolved_name, "amount": amount})
            continue
        seen_rows.add(duplicate_key)
        if is_new:
            names.append(resolved_name)
        accepted.append({"name": resolved_name, "amount": amount})

    return accepted, {"imported": len(accepted), "imported_amount": sum(item["amount"] for item in accepted), "duplicates": duplicates, "merged": merged, "rejected": rejected, "new_names": [name for name in names if name not in known_names]}