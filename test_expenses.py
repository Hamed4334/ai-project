"""
Runnable verification check for expenses analysis logic.
Tests category aggregation, monthly trend grouping, budget tracking, and CSV parsing.
"""

def aggregate_categories(expenses):
    cat_map = {}
    total = sum(e["amount"] for e in expenses)
    for e in expenses:
        cat = e["category"]
        cat_map[cat] = cat_map.get(cat, 0.0) + e["amount"]
    
    shares = {c: (amt / total * 100) if total > 0 else 0.0 for c, amt in cat_map.items()}
    return total, cat_map, shares

def aggregate_monthly(expenses):
    months = {}
    for e in expenses:
        m = e["date"][:7] # YYYY-MM
        months[m] = months.get(m, 0.0) + e["amount"]
    return months

def calculate_budget(spent, budget):
    if budget <= 0:
        return 0.0
    return round((spent / budget) * 100, 1)

def parse_csv_line(line):
    result = []
    current = ""
    in_quotes = False
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            result.append(current.strip())
            current = ""
        else:
            current += char
    result.append(current.strip())
    return result

def run_tests():
    sample = [
        {"id": "1", "title": "Rent", "amount": 1000.0, "category": "Housing", "date": "2026-09-01"},
        {"id": "2", "title": "Groceries", "amount": 250.0, "category": "Food", "date": "2026-09-05"},
        {"id": "3", "title": "Dinner", "amount": 50.0, "category": "Food", "date": "2026-08-20"},
        {"id": "4", "title": "Train", "amount": 100.0, "category": "Transport", "date": "2026-08-15"}
    ]

    total, cat_map, shares = aggregate_categories(sample)
    assert total == 1400.0, f"Expected 1400.0, got {total}"
    assert cat_map["Food"] == 300.0, f"Expected 300.0, got {cat_map['Food']}"
    assert round(shares["Housing"], 1) == 71.4, f"Expected ~71.4%, got {shares['Housing']}"

    months = aggregate_monthly(sample)
    assert months["2026-09"] == 1250.0, f"Expected 1250.0 for Sept, got {months['2026-09']}"
    assert months["2026-08"] == 150.0, f"Expected 150.0 for Aug, got {months['2026-08']}"

    pct = calculate_budget(1250.0, 2000.0)
    assert pct == 62.5, f"Expected 62.5%, got {pct}"

    csv_line = '1,"2026-09-01","Apartment Rent, Phase 1","Housing",1000.0'
    parts = parse_csv_line(csv_line)
    assert len(parts) == 5, f"Expected 5 parts, got {len(parts)}"
    assert parts[2] == "Apartment Rent, Phase 1", f"Quoted comma handling failed: {parts[2]}"

    print("All expenses analysis verification checks passed successfully!")

if __name__ == "__main__":
    run_tests()
