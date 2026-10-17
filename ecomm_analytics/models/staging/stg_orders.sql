-- Flattens the raw JSON orders into one row per order line item.
-- One row per order_line_id (order_id + position in the line_items array).

with raw_data as (
    select
        raw_payload,
        ingested_at
    from {{ source('raw_source', 'stg_orders_raw') }}
    -- Keep only the latest load of each order. Deduping here before the
    -- flatten means a reloaded order never keeps stale line items.
    qualify row_number() over (
        partition by raw_payload:order_id::string
        order by ingested_at desc
    ) = 1
),

flattened_orders as (
    select
        raw_payload:order_id::string as order_id,
        -- Position of the item within the order. This is the line key
        -- because the same product can appear on multiple lines.
        li.index as line_item_number,
        raw_payload:order_date::timestamp_ntz as order_date,
        -- Order-level total, repeated on every line of the order.
        -- Do not sum this across line items - use item_total_cost for revenue.
        raw_payload:order_total::number(10,2) as order_total,
        raw_payload:payment_status::string as payment_status,

        raw_payload:customer.customer_id::string as customer_id,
        raw_payload:customer.email::string as customer_email,
        raw_payload:customer.shipping_state::string as shipping_state,

        li.value:product_id::string as product_id,
        li.value:product_name::string as product_name,
        li.value:category::string as product_category,
        li.value:price::number(10,2) as item_price,
        li.value:quantity::int as item_quantity,
        li.value:item_total::number(10,2) as item_total_cost,

        ingested_at
    from raw_data,
    lateral flatten(input => raw_payload:line_items) as li
)

select
    -- Surrogate key so the grain can be tested without extra packages
    order_id || '-' || line_item_number as order_line_id,
    *
from flattened_orders