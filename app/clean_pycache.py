import os
import shutil

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if name.endswith(".pyc"):
            os.remove(os.path.join(root, name))
    for name in dirs:
        if name == "__pycache__":
            shutil.rmtree(os.path.join(root, name))
