# Personal Project Blueprint: E-Commerce Modern Data Stack (MDS) Pipeline

This project simulates a modern data engineering pipeline for an e-commerce/retail brand. I will ingest raw e-commerce data (orders, customer interactions, inventory), store it as semi-structured data, and transform it using the tech stack described.

## 🛠️ Architecture & Tech Stack
* **Orchestration & Ingestion:** Python (simulating Azure Data Factory or Airflow) + REST APIs
* **Data Warehouse:** Snowflake (Free Trial)
* **Transformation & Modeling:** dbt Core (Data Build Tool)
* **CI/CD & Automation:** GitHub Actions

---

## 🚀 Step-by-Step Project Implementation

### Phase 1: Mock API & Data Ingestion (Python)
Instead of paying for live retail feeds, build a local Python script that mimics an e-commerce platform's API (like Shopify or a custom warehouse management system).
1. **Generate Mock Data:** Use Python to create nested JSON payloads containing:
   * **Orders:** `order_id`, `customer_id`, `line_items` (nested array of product IDs, quantities, prices), `discount_codes`, and `order_timestamp`.
   * **Inventory:** `sku`, `warehouse_id`, `stock_level`, `updated_at`.
2. **Handle API Patterns:** Implement pagination (e.g., limit/offset or cursor-based) and rate-limiting handles in your Python extraction code.
3. **Landing the Data:** Write the extracted data incrementally into local JSON files or drop them into an AWS S3 bucket / Azure Blob Storage container as a staging area.

### Phase 2: Cloud Warehousing & JSON Parsing (Snowflake)
Set up a free-tier Snowflake account to practice loading and managing semi-structured data.
1. **Create Stages:** Set up an external stage pointing to your cloud storage, or an internal stage to upload your local mock JSON files.
2. **Ingest Raw JSON:** Load the files directly into a table with a single column of type `VARIANT`.
3. **Flatten Variant Columns:** Write SQL queries using `LATERAL FLATTEN` to extract the nested `line_items` array out of your JSON structure into a tabular format (one row per ordered item).

### Phase 3: Data Transformation & CI/CD (dbt & GitHub)
Organize your transformations using dbt to transform raw data into production-ready analytical models.
1. **Layered Modeling:**
   * **Staging Layer (`stg_`):** Flatten your raw JSON variants into structured base tables.
   * **Intermediate Layer (`int_`):** Handle delta sync adjustments (e.g., deduplicating orders or calculating line-item totals).
   * **Mart Layer (`fct_`, `dim_`):** Build a `fct_orders` table and a `dim_customers` table for business intelligence consumption.
2. **CI/CD Configuration:** Set up a GitHub repository and configure a **GitHub Actions** workflow. Program it to automatically run `dbt test` and `dbt run` on a sandbox dataset whenever you open a Pull Request.

---

## 📈 Retail Analytics Use Cases to Solve
Once your pipeline runs, write final analytical queries or connect a free visualization tool (like Lightdash or Looker Studio) to answer:
* **Abandoned Cart/Order Analytics:** Average basket size, items per order, and revenue impacts of discount codes.
* **Inventory Turnover:** Identifying low-stock items based on real-time simulated order velocity.
