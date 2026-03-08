import re
import os

html_path = r'e:\Vedavathi\dashboard\index.html'
js_path = r'e:\Vedavathi\dashboard\app.js'

functions_to_expose = set()

for path in [html_path, js_path]:
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all onclick patterns
    # Simplified search for anything that looks like onclick="..." or onclick='...'
    onclick_matches = re.findall(r'onclick\s*=\s*[\"\'](.*?)[\"\']', content)

    for pattern in onclick_matches:
        # Match function names before (
        func_matches = re.findall(r'([a-zA-Z0-9_]+)\(', pattern)
        for m in func_matches:
            # Exclude keywords
            if m not in ['if', 'for', 'while', 'console', 'alert', 'confirm', 'prompt', 'parseInt', 'parseFloat', 'isNaN', 'isFinite', 'Number', 'String', 'Boolean']:
                functions_to_expose.add(m)

print(f"Found {len(functions_to_expose)} unique functions in onclick handlers:")
for f in sorted(functions_to_expose):
    print(f"- {f}")

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

print("\nVerifying presence in app.js and generating exposure code...")
exposure_code = []
for func in sorted(functions_to_expose):
    # Check if defined as function func() or async function func()
    # or window.func = ... or func = function(...)
    if re.search(r'(async\s+)?function\s+' + func + r'\s*\(', js_content) or f'window.{func}' in js_content or re.search(r'\b' + func + r'\s*=\s*function', js_content):
        exposure_code.append(f"window.{func} = {func};")

print("\nSuggested Exposure Block:")
print("\n".join(exposure_code))
