-- PostgreSQL views. Load revenue_mart at one invoiced order-line grain.
create or replace view vw_revenue_kpis as
select date_trunc('month', order_date::date)::date as month,
       sum(net_revenue) as net_revenue,
       round(100.0 * sum(gross_margin) / nullif(sum(net_revenue),0),2) as gross_margin_pct,
       sum(leakage_value) as leakage_value,
       round(100.0 * sum(return_value) / nullif(sum(gross_revenue),0),2) as return_rate_pct
from revenue_mart group by 1 order by 1;

create or replace view vw_leakage_exception_queue as
select order_id, order_date, customer_name, product_name, region, net_revenue,
       leakage_value, leakage_score, leakage_reason
from revenue_mart where leakage_score >= 40 order by leakage_value desc, leakage_score desc;

-- Reconciliation: must return zero difference.
select sum(gross_revenue) - sum(net_revenue + return_value) as gross_to_net_difference from revenue_mart;
