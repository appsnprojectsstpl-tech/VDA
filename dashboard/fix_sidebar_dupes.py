"""
Fix duplicate sidebar entries in index.html
Remove duplicate data-page entries for: finance2, dms, bi, workflow, ticketing,
booking, lms, fieldservice, farmerportal, survey, schemes
"""

with open('dashboard/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find all menu-item blocks with data-page
# Strategy: Parse and deduplicate by tracking seen data-page values
# We'll use regex to find duplicate menu-item divs and remove them

seen = set()
result = []
i = 0
lines = content.split('\n')
skip_until = -1

i = 0
out_lines = []
while i < len(lines):
    line = lines[i]
    # Check if this line starts a menu-item with data-page
    m = re.search(r'data-page="([^"]+)"', line)
    if m and 'menu-item' in line:
        page = m.group(1)
        if page in seen:
            # Skip this block (4 lines: div open, nav-icon, nav-label, div close)
            # Look ahead to find the closing div
            j = i
            depth = 0
            while j < len(lines):
                if '<div' in lines[j]:
                    depth += lines[j].count('<div') - lines[j].count('</div')
                elif '</div>' in lines[j]:
                    depth -= 1
                if j > i and depth <= 0:
                    i = j + 1
                    break
                j += 1
            continue
        else:
            seen.add(page)
    out_lines.append(line)
    i += 1

new_content = '\n'.join(out_lines)

with open('dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

# Count remaining
import re
pages = re.findall(r'data-page="([^"]+)"', new_content)
print(f"After dedup: {len(pages)} sidebar entries")
unique = set(pages)
print(f"Unique pages: {len(unique)}")
print("All pages:", sorted(unique))
