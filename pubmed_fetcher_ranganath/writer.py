import csv
from typing import List, Dict, Any


def sanitize(value: Any) -> str:
    if value is None:
        return ""
    elif isinstance(value, str):
        return value
    elif isinstance(value, list):
        return "; ".join(sanitize(v) for v in value)
    elif isinstance(value, dict):
        parts = []
        for k, v in value.items():
            parts.append(f"{k}: {sanitize(v)}")
        return "; ".join(parts)
    else:
        return str(value)


def write_csv(data: List[Dict[str, Any]], filename: str) -> None:
    if not data:
        print("No data to write.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=data[0].keys(),
            quoting=csv.QUOTE_ALL  
        )
        writer.writeheader()

        for row in data:
            try:
                safe_row = {k: sanitize(v).replace('\n', ' ').strip() for k, v in row.items()}
                print(" Writing row:", safe_row)  # Optional debug line
                writer.writerow(safe_row)
            except Exception as e:
                print(f" Failed to write row: {row}")
                print(f" Error: {e}")

    print(f" Results written to: {filename}")
    

def print_csv(data: List[Dict[str, Any]]) -> None:
    if not data:
        print("No data to display.")
        return

    keys = data[0].keys()
    print(", ".join(keys))
    for row in data:
        values = [sanitize(row[k]) for k in keys]
        print(", ".join(values))
