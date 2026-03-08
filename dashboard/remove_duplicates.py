import re

js_path = r'e:\Vedavathi\dashboard\app.js'

with open(js_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# For each duplicate, we identify the second occurrence's start/end line (1-indexed)
# and remove it. We process from the bottom up to preserve line numbers.
# 
# Duplicates (second occurrences):
#   populatePoultrySelects: starts at 12138
#   loadPoultryTables: starts at 12172
#   vermiTab: starts at 13029
#   treeTab: starts at 13036
#   paintTab: starts at 13043
#   saveEggCollection: starts at 13479
#   savePoultryFeed: starts at 13562

def find_function_end(lines, start_idx):
    """Find the end line (1-indexed) of a function starting at start_idx (0-indexed)."""
    brace_depth = 0
    found_open = False
    for i in range(start_idx, len(lines)):
        for ch in lines[i]:
            if ch == '{':
                brace_depth += 1
                found_open = True
            elif ch == '}':
                brace_depth -= 1
        if found_open and brace_depth == 0:
            return i  # 0-indexed end line
    return len(lines) - 1

# Identify duplicate start lines (1-indexed from Python output)
duplicate_starts_1indexed = [12138, 12172, 13029, 13036, 13043, 13479, 13562]

# Convert to 0-indexed
duplicate_ranges = []
for start_1 in duplicate_starts_1indexed:
    start_0 = start_1 - 1
    end_0 = find_function_end(lines, start_0)
    duplicate_ranges.append((start_0, end_0))
    print(f"  Removing lines {start_1}–{end_0 + 1}: {lines[start_0].strip()[:60]}")

# Remove from bottom to top to preserve indices
duplicate_ranges.sort(reverse=True)
for start_0, end_0 in duplicate_ranges:
    del lines[start_0:end_0 + 1]

with open(js_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\nDone. New line count: {len(lines)}")
