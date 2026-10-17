-- One row per order - safe for summing order_total
select
    order_id,
    order_date,
    order_total,
    payment_status,
    customer_id,
    customer_email,
    shipping_state
from {{ ref('stg_orders') }}
qualify row_number() over (partition by order_id order by line_item_number) = 1