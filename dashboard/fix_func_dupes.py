"""
Clean up duplicate function definitions using a robust line-by-line approach.
Keeps first occurrence, removes subsequent ones.
"""
import re

with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Starting size: {round(len(content)/1024/1024,2)} MB")

# Find all simple function keyword declarations
# Pattern: function NAME( at start of statement
func_defs = list(re.finditer(r'\nfunction ([a-zA-Z_]\w*)\s*\(', content))

print(f"Total function defs: {len(func_defs)}")

seen = {}
to_remove = []  # list of (start, end) to remove

for m in func_defs:
    name = m.group(1)
    if name in seen:
        to_remove.append((name, m.start()))
    else:
        seen[name] = m.start()

print(f"Duplicate function names found: {[t[0] for t in to_remove]}")

# For each duplicate, find its complete body and remove it
# Process in reverse order to preserve positions
removed = 0
for name, start_pos in reversed(to_remove):
    # Find opening brace
    open_brace = content.index('{', start_pos)
    # Walk to matching close brace
    depth = 0
    i = open_brace
    while i < len(content):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                end_pos = i + 1
                # Remove the block (from newline before function to end)
                block = content[start_pos:end_pos]
                content = content[:start_pos] + content[end_pos:]
                removed += 1
                print(f"  Removed duplicate: {name} ({len(block)} chars)")
                break
        i += 1

print(f"\nRemoved {removed} duplicate functions")

with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    final = f.read()

print(f"Final size: {round(len(final)/1024/1024,2)} MB")

# Final check
all_tabs = ['crmTab','hrmTab','invTab','finTab','dmsTab','biTab','wfTab','ticketTab',
            'bookingTab','lmsTab','fsTab','fpTab','surveyTab','schemeTab',
            'gridTab','solarTab','windTab','biogasTab','hydrogenTab','hydroTab',
            'kineticTab','cattleTab','poultryTab','aquaTab','vermiTab','treeTab',
            'paintTab','carbonTab','tourismTab','vetTab','vedicTab','financeTab',
            'logisticsTab','waterTab','trustTab','commandTab']

missing = [t for t in all_tabs if t not in final]
print(f"\nMissing tab functions: {missing if missing else 'NONE - all present!'}")
print(f"Total tab functions accounted for: {len(all_tabs) - len(missing)}/{len(all_tabs)}")
