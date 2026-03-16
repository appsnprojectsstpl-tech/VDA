"""Trace brace balances to find the syntax error"""
with open('app.js', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

balance = 0
positive_start = None
last_n_balance_states = []

for i, line in enumerate(lines, 1):
    open_b = line.count('{')
    close_b = line.count('}')
    old_bal = balance
    balance += open_b - close_b

    if balance > 0 and old_bal == 0:
        positive_start = i

    # Keep track of last 50 balance states
    if i > len(lines) - 3000:
        last_n_balance_states.append((i, balance, open_b - close_b))

# Find where the positive balance started
if balance > 0:
    print(f"Final balance: {balance}")
    print(f"Final positive section started at line: {positive_start}")

    # Find the last time balance returned to 0 before staying positive
    prior_zero = None
    bal = 0
    for i, line in enumerate(lines, 1):
        open_b = line.count('{')
        close_b = line.count('}')
        bal += open_b - close_b

        if i < positive_start and bal == 0:
            prior_zero = i

    print(f"Last 0 balance before positive_start: {prior_zero}")

    # Show context around the positive_start
    print(f"\nContext around line {positive_start}:")
    for offset in range(-5, 6):
        idx = positive_start + offset - 1
        if 0 <= idx < len(lines):
            open_b = lines[idx].count('{')
            close_b = lines[idx].count('}')
            print(f"  Line {idx+1} ({open_b - close_b}): {repr(lines[idx][:80])}")
