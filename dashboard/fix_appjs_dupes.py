"""
Fix duplicate page keys in app.js pages object.
Also check for duplicate function definitions.
"""

with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find all page key definitions: lines like '    key: `'
# Pattern: 4 spaces, word, colon, space, backtick
pattern = r'^    ([a-zA-Z0-9_]+): `'
matches = list(re.finditer(pattern, content, re.MULTILINE))

print(f"Total page key definitions: {len(matches)}")

# Find duplicates
seen = {}
duplicates = []
for m in matches:
    key = m.group(1)
    if key in seen:
        duplicates.append((key, m.start(), seen[key]))
    else:
        seen[key] = m.start()

print(f"Duplicate page keys: {[d[0] for d in duplicates]}")

if not duplicates:
    print("No duplicates found in app.js!")
else:
    # Remove duplicate page entries by finding each duplicate's full template block
    # and removing the SECOND occurrence (keep first, remove later)
    # Process from end to beginning to preserve positions
    
    # For each duplicate, find the complete template (from key: ` ... `,)
    content_modified = content
    removed_count = 0
    
    for key, dup_pos, orig_pos in reversed(duplicates):
        # Find the duplicate occurrence's start and end
        # Start: the line with '    key: `'
        # End: the closing '`,'  or  '`\n\n' at the same indent level
        
        # Find newline before dup_pos to get line start
        line_start = content_modified.rfind('\n', 0, dup_pos) + 1
        
        # Find the end of this template block
        # Look for the pattern: backtick followed by comma at column 4
        search_from = dup_pos + len(key) + 5
        end_pattern = re.compile(r'\n    `\s*,', re.MULTILINE)
        end_match = end_pattern.search(content_modified, search_from)
        
        if end_match:
            block_end = end_match.end()
            removed_block = content_modified[line_start:block_end]
            print(f"\nRemoving duplicate '{key}' block ({len(removed_block)} chars)")
            content_modified = content_modified[:line_start] + content_modified[block_end:]
            removed_count += 1
        else:
            print(f"Could not find end of duplicate '{key}' block")
    
    with open('dashboard/app.js', 'w', encoding='utf-8') as f:
        f.write(content_modified)
    
    print(f"\nRemoved {removed_count} duplicate page blocks")
    
    # Verify
    with open('dashboard/app.js', 'r', encoding='utf-8') as f:
        content_new = f.read()
    
    new_matches = list(re.finditer(pattern, content_new, re.MULTILINE))
    print(f"Page keys after cleanup: {len(new_matches)}")
    print(f"New app.js size: {round(len(content_new)/1024/1024, 2)} MB")
