{{ config(materialized='table') }}

with staging_orders as (
    select * from {{ ref('stg_orders') }}
),

product_aggregates as (
    select
        product_id,
        product_name,
        product_category,
        -- Calculate clean business KPIs
        sum(item_quantity) as total_units_sold,
        sum(item_total_cost) as total_gross_revenue,
        count(distinct order_id) as unique_orders_count,
        round(avg(item_quantity), 2) as average_basket_quantity
    from staging_orders
    where payment_status = 'PAID' -- Only analyze successful revenue!
    group by 1, 2, 3
)

select * from product_aggregates
order by total_gross_revenue desc
