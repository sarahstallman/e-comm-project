# Project Blueprint: E-Commerce Data Pipeline

I am a Data Engineer with 2+ years of experience building large-scale data solutions for government clients in a technical consulting environment. My goal is to transition into the retail industry, specifically apparel or beauty, where I can apply my skills to products and brands I have genuine interest in. The purpose of this repository is for me to build hands-on experience with industry-relevant data tools and practices outside of what I use in my current role.

This project simulates a data engineering pipeline for an e-commerce/retail brand. Raw e-commerce data (orders, customer interactions, inventory) is ingested, stored as semi-structured data, and transformed it using the tech stack described.

## Architecture & Tech Stack
* **Orchestration & Ingestion:** Python (simulating Azure Data Factory or Airflow) + REST APIs
* **Data Warehouse:** Snowflake
* **Transformation & Modeling:** dbt Core (Data Build Tool)
* **CI/CD & Automation:** GitHub Actions

---

## Step-by-Step Project Implementation

### Phase 1: Mock API & Data Ingestion (Python)
Build a local Python script that mimics an e-commerce platform's API
1. **Generate Mock Data:** Use Python to create nested JSON payloads containing:
   * **Orders:** order_id, customer_id, line_items (nested array of product IDs, quantities, prices), discount_codes, and order_timestamp.
   * **Inventory:** sku, warehouse_id, stock_level, updated_at.
2. **Handle API Patterns:** Implement pagination and rate-limiting handles in extraction code.
3. **Landing the Data:** Write the extracted data incrementally into local JSON files or drop them into an Azure Blob Storage container as a staging area.

### Phase 2: Cloud Warehousing & JSON Parsing (Snowflake)
Use Snowflake to load and manage semi-structured data.
1. **Create Stages:** Set up an external stage pointing to cloud storage.
2. **Ingest Raw JSON:** Load the files directly into a table with a single VARIANT column.
3. **Flatten Variant Columns:** Write SQL queries using LATERAL FLATTEN to extract the nested line_items array out of the JSON structure into a tabular format (one row per ordered item).

### Phase 3: Data Transformation & CI/CD (dbt & GitHub)
Organize transformations using dbt to transform raw data into analytical models.
1. **Layered Modeling:**
   * **Staging Layer (stg_):** Flatten raw JSON variants into structured base tables.
   * **Intermediate Layer (int_):** Handle delta sync adjustments (deduplicating orders, calculating line-item totals).
   * **Mart Layer (fact_, dim_):** Build a fact_orders table and a dim_customers table for business intelligence consumption.
2. **CI/CD Configuration:** Set up a GitHub repository and configure a **GitHub Actions** workflow. Program it to automatically run dbt test and dbt run on a sandbox dataset whenever a pull request is opened.

---

## Retail Analytics Use Cases to Solve
Once the pipeline runs, write final analytical queries to answer:
* **Abandoned Cart/Order Analytics:** Average basket size, items per order, and revenue impacts of discount codes.
* **Inventory Turnover:** Identifying low-stock items based on real-time simulated order velocity.

