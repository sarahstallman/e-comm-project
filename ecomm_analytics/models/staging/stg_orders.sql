{{ config(materialized='table') }}

with raw_data as (
    select
        raw_payload,
        ingested_at
    from {{ source('raw_source', 'stg_orders_raw') }}
),

flattened_orders as (
    select
        -- Extract top-level fields from the JSON variant using the ':' operator
        raw_payload:order_id::string as order_id,
        raw_payload:order_date::timestamp_ntz as order_date,
        raw_payload:order_total::float as order_total,
        raw_payload:payment_status::string as payment_status,

        -- Extract nested customer objects
        raw_payload:customer.customer_id::string as customer_id,
        raw_payload:customer.email::string as customer_email,
        raw_payload:customer.shipping_state::string as shipping_state,

        -- Unpack individual line items from the nested array
        value:product_id::string as product_id,
        value:product_name::string as product_name,
        value:category::string as product_category,
        value:price::float as item_price,
        value:quantity::int as item_quantity,
        value:item_total::float as item_total_cost,

        ingested_at
    from raw_data,
    -- LATERAL FLATTEN explodes the JSON list into standard rows
    lateral flatten(input => raw_payload:line_items)
)

select * from flattened_orders
