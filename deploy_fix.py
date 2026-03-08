import re
import os
import shutil

# Fix index.html
with open('dashboard/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'<script\s+src=["\']validate_navigation\.js["\']></script>', '', html)
html = re.sub(r'<script\s+src=["\']final_validation\.js["\']></script>', '', html)

with open('dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Cleaned index.html tags.")

# Prepare the deployment folder again
src = 'dashboard'
dest = 'E:/tmp_vedavathi_deploy'

if os.path.exists(dest):
    shutil.rmtree(dest)
os.makedirs(dest)

# Copy everything from dashboard
for f in os.listdir(src):
    s = os.path.join(src, f)
    d = os.path.join(dest, f)
    if os.path.isfile(s) and f.endswith(('.js', '.html', '.css', '.json', '.png')):
        shutil.copy2(s, d)

print('Clean build folder created at', dest)
print('Total deployable files:', len(os.listdir(dest)))
