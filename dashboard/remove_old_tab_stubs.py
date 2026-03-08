import re

js_path = r'e:\Vedavathi\dashboard\app.js'
with open(js_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# aqTab old stub: starts at L13116 (0-indexed 13115)
# vetTab old stub: starts at L10540 (0-indexed 10539)
# Remove them from bottom-up using find_function_end

def find_function_end(lines, start_idx):
    brace_depth = 0
    found_open = False
    for i in range(start_idx, min(len(lines), start_idx + 30)):
        for ch in lines[i]:
            if ch == '{': brace_depth += 1; found_open = True
            elif ch == '}': brace_depth -= 1
        if found_open and brace_depth == 0:
            return i
    return start_idx + 5

# Find actual line numbers by searching for the patterns
aqtab_line = None
vettab_line = None
for i, line in enumerate(lines):
    if i > 13000 and 'function aqTab' in line and aqtab_line is None:
        aqtab_line = i
    if i > 10000 and 'function vetTab' in line and vettab_line is None:
        vettab_line = i

print(f"aqTab old stub at 0-indexed line: {aqtab_line}")
print(f"vetTab old stub at 0-indexed line: {vettab_line}")

removals = []
if aqtab_line:
    end = find_function_end(lines, aqtab_line)
    removals.append((aqtab_line, end))
    print(f"  Will remove aqTab: L{aqtab_line+1}-{end+1}")
if vettab_line:
    end = find_function_end(lines, vettab_line)
    removals.append((vettab_line, end))
    print(f"  Will remove vetTab: L{vettab_line+1}-{end+1}")

# Remove from bottom-up
removals.sort(reverse=True)
for start, end in removals:
    del lines[start:end+1]

with open(js_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Done. New line count: {len(lines)}")
