import re

js_path = r'e:\Vedavathi\dashboard\app.js'
html_path = r'e:\Vedavathi\dashboard\index.html'

with open(js_path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()
    lines = content.split('\n')

with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()
    html_lines = html.split('\n')

all_text = content + html

# ── Find ALL onclick= in the combined script ──
onclick_pattern = re.compile(r'onclick=["\']([^"\']+)["\']')

func_calls = {}
for m in onclick_pattern.finditer(all_text):
    for func_m in re.findall(r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(', m.group(1)):
        if func_m not in ('if','for','while','function','return','new','console','alert','confirm','parseInt','parseFloat','this','event','document','window','typeof','void'):
            if func_m not in func_calls:
                func_calls[func_m] = []
            func_calls[func_m].append(m.group(1)[:60])

print(f"=== {len(func_calls)} unique functions in onclick handlers ===\n")

missing = []
for func in sorted(func_calls.keys()):
    in_window = f'window.{func}' in content
    is_decl = bool(re.search(r'(async\s+)?function\s+' + re.escape(func) + r'\s*\(', content))
    is_expr = bool(re.search(re.escape(func) + r'\s*=\s*(async\s+)?function', content))
    defined = in_window or is_decl or is_expr
    if not defined:
        missing.append(func)

print(f"=== MISSING functions ({len(missing)}) ===")
for f in missing:
    print(f"  MISSING: {f}")
    # Show one example onclick
    if func_calls[f]:
        print(f"    Example onclick: {func_calls[f][0]}")

print("\n=== Checking Aqua/Vet/Vedic specifically ===")
# Look in the HTML sidebar for these nav items
for term in ['aqua', 'vet', 'vedic']:
    print(f"\n-- Searching for '{term}' in index.html --")
    for i, line in enumerate(html_lines, 1):
        if term.lower() in line.lower() and ('onclick' in line.lower() or 'href' in line.lower() or 'showPage' in line):
            print(f"  L{i}: {line.strip()[:130]}")

    print(f"-- Searching for '{term}' in app.js sidebar/nav --")
    for i, line in enumerate(lines, 1):
        if term.lower() in line.lower() and 'onclick' in line.lower():
            print(f"  L{i}: {line.strip()[:130]}")
