import os
import re

# Define paths
PROJECT_NAME = '/tokenshare-svelte'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + PROJECT_NAME
settings_path = os.path.join(BASE_DIR, 'core','settings.py')
env_path = os.path.join(BASE_DIR, '.env')

print(f"BASE_DIR is set to: {BASE_DIR}")
print(f"Expecting .env file at: {env_path}")

# Create .env file if it does not exist
if not os.path.isfile(env_path):
    with open(env_path, 'a') as file:
        file.write('# .env\n')
    print(f".env file created at {env_path}")
else:
    print(".env file already exists.")

# Read settings.py
with open(settings_path, 'r') as file:
    settings_content = file.readlines()

# Prepare the new dotenv import lines
dotenv_import_lines = [
    'from dotenv import load_dotenv\n',
    'import os\n',
    'load_dotenv()\n\n'
]

# Prepare the SECRET_KEY replacement line
# secret_key_pattern = r"^(SECRET_KEY = '.+')$"
secret_key_pattern = r'^SECRET_KEY = ["\'](.+)["\']$'
secret_key_env = "SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')\n"

# Flags
secret_key_found = False

# Search for the SECRET_KEY and dotenv imports
for i, line in enumerate(settings_content):
    match = re.match(secret_key_pattern, line)
    if match:
        # Extract the actual secret key value and replace the line
        # secret_key = match.group(1).split('=')[1].strip().strip("'")
        secret_key = line.split('=')[1].strip().strip("'\"")
        settings_content[i] = secret_key_env
        secret_key_found = True
        break

# Insert dotenv imports at the top of settings.py if not already present

# Reverse to keep order when inserting
for i, line in enumerate(dotenv_import_lines[::-1]):
    settings_content.insert(0, line)

if secret_key_found:
    # Write the modified settings.py content
    with open(settings_path, 'w') as file:
        file.writelines(settings_content)

    # Append the SECRET_KEY to the .env file
    with open(env_path, 'a') as file:
        file.write(f'DJANGO_SECRET_KEY={secret_key}\n')
    print("SECRET_KEY has been moved to .env and settings.py has been updated.")
else:
    print("SECRET_KEY not found in your settings.py file.")
