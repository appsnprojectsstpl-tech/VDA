"""
Fix the showUserProfile function closure bug in app.js.
"""
import sys

with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

bad_open = "window.showUserProfile = typeof showUserProfile === 'function' ? showUserProfile : window.showUserProfile || function () {\n\n    // ============================================\n    // TIER 3 - BOOKING & RESERVATION MODULE\n    // ============================================\n    booking: `"

if bad_open not in content:
    print("ERROR: pattern not found")
    sys.exit(1)

start = content.find("window.showUserProfile = typeof showUserProfile === 'function' ? showUserProfile : window.showUserProfile || function () {")
print(f"Bad block starts at char: {start}")

# Find the end - the orphaned Tier 3 templates end just before the next tab function block
end_marker = "\nfunction biogasTab"
orphan_end = content.find(end_marker, start)
if orphan_end == -1:
    print("Could not find end marker biogasTab")
    # Try alternate
    end_marker = "\n// ── BIOGAS TAB SWITCHER"
    orphan_end = content.find(end_marker, start)
    if orphan_end == -1:
        print("Could not find alternate end marker")
        sys.exit(1)

print(f"Orphaned block ends at char: {orphan_end}")
print(f"Orphaned block size: {orphan_end - start} chars")

# Replacement: close the function properly
correct_line = "window.showUserProfile = typeof showUserProfile === 'function' ? showUserProfile : window.showUserProfile || function () { };"

new_content = content[:start] + correct_line + content[orphan_end:]

with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed!")
print(f"New size: {round(len(new_content)/1024/1024, 2)} MB")

# Verify
with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    final = f.read()

ok1 = "showUserProfile || function () { };" in final
ok2 = "booking: `" in final
print(f"showUserProfile closed: {ok1}")
print(f"booking template preserved: {ok2}")
