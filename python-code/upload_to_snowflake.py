import os
import json
import sys
import snowflake.connector
from dotenv import load_dotenv

# Resolve the .env path relative to this script so it loads regardless of
# which directory the script is run from
script_dir = os.path.dirname(os.path.abspath(__file__))  # python-code/
project_root = os.path.dirname(script_dir)               # project root
env_path = os.path.join(project_root, ".env")            # path to .env

# Load Snowflake credentials into environment variables so they never
# need to be hardcoded in the script
load_dotenv(dotenv_path=env_path)


def upload_json_to_snowflake():
    """Read the locally generated orders JSON and load each order into
    Snowflake as a single variant value in the raw staging table."""

    # Establish path to data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    json_path = os.path.join(project_root, "raw-data", "raw_orders_data.json")

    # Fail early if the generator hasn't been run yet
    if not os.path.exists(json_path):
        print(f"Error: Could not find raw file at {json_path}. Run generate_orders.py first.")
        return

    # Load the local JSON file into memory as a list of order dicts
    with open(json_path, "r") as f:
        orders_list = json.load(f)

    print(f"Read {len(orders_list)} orders from local file. Connecting to Snowflake...")

    # Establish connection to Snowflake
    # All values come from the .env file
    conn = snowflake.connector.connect(
        account=os.getenv("SF_ACCOUNT"),
        user=os.getenv("SF_USER"),
        password=os.getenv("SF_PASSWORD"),
        role=os.getenv("SF_ROLE"),
        warehouse=os.getenv("SF_WAREHOUSE"),
        database=os.getenv("SF_DATABASE"),
        schema=os.getenv("SF_SCHEMA")
    )

    cursor = conn.cursor()

    try:
        print("Connected! Preparing data stream...")

        # Clear previous loads so each run is a full refresh instead of
        # appending duplicates
        cursor.execute("TRUNCATE TABLE STG_ORDERS_RAW")

        insert_query = "INSERT INTO STG_ORDERS_RAW (raw_payload) SELECT PARSE_JSON(%s)"
        for order in orders_list:
            cursor.execute(insert_query, (json.dumps(order),))

        print(f"Success! Uploaded all {len(orders_list)} nested orders into Snowflake.")

    except Exception as e:
        print(f"Ingestion Error: {str(e)}")
        sys.exit(1)  # nonzero exit so a workflow would fail visibly

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    upload_json_to_snowflake()