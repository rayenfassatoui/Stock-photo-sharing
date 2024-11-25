import os

dirs = ['static', 'media', 'staticfiles']
base_dir = os.path.dirname(os.path.abspath(__file__))

for dir_name in dirs:
    dir_path = os.path.join(base_dir, dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")
    else:
        print(f"Directory already exists: {dir_path}")
