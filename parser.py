import re
import pandas as pd

def clean_text(text):
    lines = text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]
    return lines


def parse_receipt(text):
    lines = clean_text(text)
    data = []

    for line in lines:

        # Skip time format (3:29)
        if re.search(r"\d+:\d+", line):
            continue

        # Match price with dollar sign
        match = re.search(r"(.+?)\s*\$?(\d+\.\d{2})", line)

        if match:
            item = match.group(1).strip()
            price = float(match.group(2))

            # Remove unwanted words
            if any(word in item.lower() for word in ["total", "change", "thank", "receipt"]):
                continue

            data.append({
                "Item": item,
                "Price": price,
                "Quantity": 1
            })

    return pd.DataFrame(data)
