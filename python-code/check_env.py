import os
from dotenv import load_dotenv

# Find the root directory path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
env_path = os.path.join(project_root, ".env")

print(f"Looking for .env file at: {env_path}")
print(f"Does the file physically exist there? {os.path.exists(env_path)}")

# Attempt to load the file
load_dotenv(dotenv_path=env_path)

# Print variables out to the console (Hiding passwords for safety)
print("\n--- Environmental Values Read By Python ---")
print(f"SF_ACCOUNT: {os.getenv('SF_ACCOUNT')}")
print(f"SF_USER:    {os.getenv('SF_USER')}")
print(f"SF_ROLE:    {os.getenv('SF_ROLE')}")
print(f"SF_PASSWORD Is Set? {'Yes (Hidden)' if os.getenv('SF_PASSWORD') else 'No (EMPTY!)'}")
