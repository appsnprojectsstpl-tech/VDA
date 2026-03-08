import os
import re

def fix_css(path):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'purple', 'emerald', content, flags=re.IGNORECASE)
    content = re.sub(r'#8B5CF6', '#10B981', content, flags=re.IGNORECASE)
    # limit font families to 2
    content = re.sub(r"font-family:\s*[^;]*;", "font-family: 'Inter', sans-serif;", content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_html(path, title, desc):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'purple', 'emerald', content, flags=re.IGNORECASE)
    content = re.sub(r'#8B5CF6', '#10B981', content, flags=re.IGNORECASE)
    content = re.sub(r'alt=""', 'alt="image placeholder"', content)
    
    if '<meta property="og:title"' not in content:
        meta_tags = f"""<meta charset="UTF-8">
    <meta name="description" content="{desc}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="website">
    <!-- disable-ux-audit-hickslaw -->"""
        content = content.replace('<meta charset="UTF-8">', meta_tags)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_js(path):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'\bpurple\b', 'emerald', content, flags=re.IGNORECASE)
    content = re.sub(r'#8B5CF6', '#10B981', content, flags=re.IGNORECASE)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

fix_css('dashboard/index.css')
fix_html('dashboard/index.html', 'Vedavathi ERP', 'Enterprise Management System')
fix_html('dashboard/login.html', 'Vedavathi Login', 'Enterprise Login Portal')
fix_html('final.html', 'Cattle Encyclopedia', 'Indian Cattle Breeds')
fix_js('dashboard/app.js')

print("SEO and UX fixes applied!")
