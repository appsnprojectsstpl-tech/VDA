"""Find syntax errors in app.js"""
with open('app.js', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Track brace balance
balance = 0
for i, line in enumerate(lines, 1):
    for char in line:
        if char == '{':
            balance += 1
        elif char == '}':
            balance -= 1

    # Report line if balance changed
    if '{' in line or '}' in line:
        if i % 2000 == 0:
            print(f'Line {i}: Balance = {balance}, Content: {line[:60]}')

# Find final state
balance = 0
for i, line in enumerate(lines, 1):
    for char in line:
        if char == '{':
            balance += 1
        elif char == '}':
            balance -= 1

print(f'\nFinal brace balance: {balance}')

# Find last lines with opening braces
balance = 0
for i, line in enumerate(lines, 1):
    open_b = line.count('{')
    close_b = line.count('}')
    balance += open_b - close_b

print(f'Total unclosed braces: {balance}')

# Show last 200 lines where balance might be positive
balance = 0
for i in range(len(lines) - 200, len(lines)):
    line = lines[i]
    open_b = line.count('{')
    close_b = line.count('}')
    balance += open_b - close_b
    if open_b > 0 or close_b > 0:
        print(f'Line {i+1}: balance={balance}, {line.strip()[:80]}')
