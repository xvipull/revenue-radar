# Data dictionary

| Table | Key | Important fields |
|---|---|---|
| `orders` | `order_id` | order_date, customer_id, product_id, quantity, invoiced_unit_price, discount_pct, cogs_unit_price |
| `price_list` | product_id | list_price, approved_discount_pct |
| `returns` | return_id | order_id, return_value, return_reason |
| `customers` | customer_id | customer_name, segment, region |
| `revenue_mart` | order_id | governed measures, flags, leakage_score, leakage_reason |

The revenue mart is at **one invoiced order line per row**. `return_value` is zero where no matching return exists.

