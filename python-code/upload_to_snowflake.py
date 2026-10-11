import os
import json
import snowflake.connector
from dotenv import load_dotenv

# Load credentials from your local secret .env file
load_dotenv()


def upload_json_to_snowflake():
    # 1. Establish pathing to your data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    json_path = os.path.join(project_root, "raw-data", "raw_orders_data.json")

    # Verify the raw file exists before starting
    if not os.path.exists(json_path):
        print(f"Error: Could not find raw file at {json_path}. Run generate_orders.py first.")
        return

    # Load the local JSON file into memory
    with open(json_path, "r") as f:
        orders_list = json.load(f)

    print(f"Read {len(orders_list)} orders from local file. Connecting to Snowflake...")

    # 2. Establish connection to Snowflake
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

        # 3. Stream data row-by-row into the VARIANT table
        # We convert the Python dictionary to a JSON string so Snowflake can parse it
        insert_query = "INSERT INTO STG_ORDERS_RAW (raw_payload) SELECT PARSE_JSON(%s)"

        for order in orders_list:
            json_string = json.dumps(order)
            cursor.execute(insert_query, (json_string,))

        print(f"Success! Uploaded all {len(orders_list)} nested orders into Snowflake.")

    except Exception as e:
        print(f"Ingestion Error: {str(e)}")

    finally:
        # Clean up database pipelines
        cursor.close()
        conn.close()


if __name__ == "__main__":
    upload_json_to_snowflake()
