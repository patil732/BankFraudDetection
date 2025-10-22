from bs4 import BeautifulSoup
import csv
import re
import random
from dateutil import parser
import logging


INPUT_FILE = r"C:\Code Repo\BankFraudDetection\extract_csv\gaurav_activity.html"
OUTPUT_FILE = "gaurav.csv"
DEVICE_NAME = "one plus"
LOCATIONS = ["Shirpur", "Dhule", "Dondaicha", "Indave"]

logging.basicConfig(level=logging.INFO, format="%(message)s")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")


divs = soup.find_all("div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")

transactions = []
current_block = []

for div in divs:
    text = div.get_text(" ", strip=True)
    if re.search(r"\b(paid|received|failed|Transaction ID|Ref ID)\b", text, re.IGNORECASE):
        if current_block:
            transactions.append(" ".join(current_block))
        current_block = [text]
    else:
        if current_block:
            current_block.append(text)

if current_block:
    transactions.append(" ".join(current_block))

# Regex patterns
date_patterns = [
    r"([A-Za-z]{3,9} \d{1,2}, \d{4})",
    r"(\d{1,2} [A-Za-z]{3,9} \d{4})",
]
time_patterns = [
    r"([0-9]{1,2}:[0-9]{2} ?[APap][Mm])",
    r"([0-9]{1,2}:[0-9]{2})",
]

def extract_date_time(text):
    date, time = "", ""
    for dp in date_patterns:
        m = re.search(dp, text)
        if m:
            date = m.group(1)
            break
    for tp in time_patterns:
        m = re.search(tp, text)
        if m:
            time = m.group(1)
            break
    return date, time

rows = []
seen_ids = set()

for tx in transactions:
    row = {
        "amount": "",
        "date": "",
        "time": "",
        "transaction_status": "Unknown",
        "transaction_id": "",
        "merchant_name": "",
        "device_name": DEVICE_NAME,
        "is_fraud": "0",
        "location": random.choice(LOCATIONS),
    }

    amt_match = re.search(r"₹\s?([\d,]+\.?\d*)", tx)
    if amt_match:
        amt = amt_match.group(1).replace(",", "")
        row["amount"] = amt

    merch_match = re.search(r"(?:to|from)\s+(.+?)(?:₹|\bTransaction|\bRef ID|$)", tx, re.IGNORECASE)
    if merch_match:
        row["merchant_name"] = merch_match.group(1).strip()

    if re.search(r"fail|declin|unsuccessful", tx, re.IGNORECASE):
        row["transaction_status"] = "Failed"
    elif re.search(r"paid|received|success", tx, re.IGNORECASE):
        row["transaction_status"] = "Success"

    id_match = re.search(r"(?:Transaction ID|Ref ID|UPI ID|Details)[:\s]*([A-Za-z0-9\-_:]+)", tx, re.IGNORECASE)
    if id_match:
        row["transaction_id"] = id_match.group(1).strip()

    d, t = extract_date_time(tx)
    if d:
        try:
            row["date"] = str(parser.parse(d).date())
        except Exception:
            row["date"] = d
    if t:
        row["time"] = t

    row["is_fraud"] = str(random.choices(["0", "1"], weights=[95, 5])[0])

    tid = row["transaction_id"] or f"{row['amount']}_{row['date']}_{row['merchant_name']}"
    if tid in seen_ids:
        continue
    seen_ids.add(tid)

    rows.append(row)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
        "amount", "date", "time", "transaction_status",
        "transaction_id", "merchant_name", "device_name",
        "is_fraud", "location"
    ])
    writer.writeheader()
    writer.writerows(rows)

logging.info(f"✅ Extracted {len(rows)} unique transactions → {OUTPUT_FILE}")
