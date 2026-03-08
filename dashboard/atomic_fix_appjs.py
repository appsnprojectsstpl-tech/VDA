"""
Atomic two-phase fix for app.js:
Phase 1: Remove orphaned Tier 3 block from inside showUserProfile
Phase 2: Inject clean Tier 3 templates into the pages object
"""
import re
import os

with open('dashboard/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Starting size: {round(len(content)/1024/1024,2)} MB")

# ─── PHASE 1: Remove orphaned block ────────────────────────────────
BAD_OPENER = "window.showUserProfile = typeof showUserProfile === 'function' ? showUserProfile : window.showUserProfile || function () { \n"
bad_pos = content.find(BAD_OPENER)
if bad_pos == -1:
    BAD_OPENER = "window.showUserProfile = typeof showUserProfile === 'function' ? showUserProfile : window.showUserProfile || function () {\n"
    bad_pos = content.find(BAD_OPENER)

if bad_pos != -1:
    # Find the end of the orphaned block
    search_from = bad_pos + len(BAD_OPENER)
    end_markers = ["\nfunction biogasTab(", "\nfunction commandTab(", "\n// === END OF"]
    orphan_end = -1
    for em in end_markers:
        idx = content.find(em, search_from)
        if idx != -1:
            orphan_end = idx
            break
    if orphan_end != -1:
        good_line = "window.showUserProfile = typeof showUserProfile === 'function' ? showUserProfile : window.showUserProfile || function () { };"
        content = content[:bad_pos] + good_line + "\n" + content[orphan_end:]
        print(f"Phase 1: Removed orphaned block. Size now {round(len(content)/1024/1024,2)} MB")
    else:
        print("Phase 1: Could not find orphan end marker")
else:
    print("Phase 1: Bad pattern not found (already fixed)")

# ─── PHASE 2: Check which Tier 3 pages are missing ──────────────────
tier3_keys = ['booking', 'lms', 'fieldservice', 'farmerportal', 'survey', 'schemes']
missing = [k for k in tier3_keys if not re.search(rf'^\s+{k}: `', content, re.MULTILINE)]
print(f"Missing from pages: {missing}")

if missing:
    # Read the templates from external file (avoids emoji encoding issues in Python source)
    tpl_file = 'dashboard/tier3_templates.js'
    if not os.path.exists(tpl_file):
        print(f"ERROR: {tpl_file} not found. Run generate_tier3_templates.py first.")
        exit(1)
    with open(tpl_file, 'r', encoding='utf-8') as f:
        tpl_content = f.read()
    
    # Find each template in the tpl file and extract it
    # Format in tpl_file: // TPL:booking\n    booking: `...`,
    insertions = []
    for key in missing:
        marker = f'// TPL:{key}'
        start_idx = tpl_content.find(marker)
        if start_idx == -1:
            print(f"  Template for {key} not found in tier3_templates.js")
            continue
        # Find the start of the template key line
        key_start = tpl_content.find(f'\n    {key}: `', start_idx)
        if key_start == -1:
            print(f"  Could not find key line for {key}")
            continue
        # Find the end: closing backtick + comma
        # Walk through template literal
        tstart = tpl_content.index('`', key_start)
        depth_t = 0
        j = tstart
        while j < len(tpl_content):
            if tpl_content[j] == '`':
                if j == tstart:
                    depth_t = 1
                elif tpl_content[j-1] != '\\':
                    depth_t -= 1
                    if depth_t == 0:
                        tend = j + 1
                        break
            j += 1
        template_block = tpl_content[key_start:tend]
        insertions.append(template_block)
        print(f"  Extracted template for {key} ({len(template_block)} chars)")
    
    if insertions:
        # Find the pages object closing brace
        pages_match = re.search(r'const pages\s*=\s*\{', content)
        if not pages_match:
            print("ERROR: pages object not found!")
            exit(1)
        
        # Walk the pages object to find its closing brace
        depth = 0
        in_tpl = False
        i = pages_match.start()
        pages_end = -1
        while i < len(content):
            ch = content[i]
            if not in_tpl:
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        pages_end = i
                        break
                elif ch == '`':
                    in_tpl = True
            else:
                if ch == '`' and content[i-1] != '\\':
                    in_tpl = False
            i += 1
        
        if pages_end == -1:
            print("ERROR: could not find pages object closing brace!")
            exit(1)
        
        print(f"Pages object closing brace at char {pages_end}")
        
        # Insert all templates just before the closing brace
        inject_text = ',\n\n' + ',\n\n'.join(insertions) + '\n'
        content = content[:pages_end] + inject_text + content[pages_end:]
        print(f"Injected {len(insertions)} templates. Size now {round(len(content)/1024/1024,2)} MB")

# Write result
with open('dashboard/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nFinal size: {round(len(content)/1024/1024,2)} MB")

# Verify
missing_check = [k for k in tier3_keys if not re.search(rf'^\s+{k}: `', content, re.MULTILINE)]
print(f"Still missing: {missing_check if missing_check else 'None'}")
bad_still = "showUserProfile || function () {\n\n    // ============" in content or "showUserProfile || function () { \n\n    // ============" in content
print(f"showUserProfile bad pattern: {'STILL PRESENT!' if bad_still else 'CLEAN'}")
