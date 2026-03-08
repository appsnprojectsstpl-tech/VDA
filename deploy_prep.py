import os
import shutil
import json

src = 'E:/Vedavathi/dashboard'
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

# Add a package.json to make Vercel happy
pkg = {
  "name": "vedavathi-dashboard",
  "version": "1.0.0",
  "scripts": {
    "build": "echo Build successful!"
  }
}

with open(os.path.join(dest, 'package.json'), 'w') as f:
    json.dump(pkg, f, indent=2)

print('Clean build folder created at', dest)
print('Total files:', len(os.listdir(dest)))
