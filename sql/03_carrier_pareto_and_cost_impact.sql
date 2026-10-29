-- ==============================================================================
-- PROJECT 2: Order-to-Delivery Process & SLA Bottleneck Optimization
-- SCRIPT: 03_carrier_pareto_and_cost_impact.sql
-- DESCRIPTION: 80/20 Pareto analysis and direct financial dispute loss attribution
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Financial Impact of SLA Breaches (Refunds & Compensation)
-- Quantifies the dollar cost of customer compensation due to missed SLAs
-- ------------------------------------------------------------------------------
SELECT 
    warehouse_hub,
    carrier_name,
    COUNT(order_id) AS total_orders,
    SUM(is_sla_breach) AS breached_orders,
    SUM(CASE WHEN dispute_filed = 'Yes' THEN 1 ELSE 0 END) AS customer_disputes,
    ROUND(SUM(CASE WHEN dispute_filed = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / SUM(is_sla_breach), 2) AS breach_to_dispute_conversion_pct,
    ROUND(SUM(refund_compensation_cost), 2) AS total_refund_payout_usd
FROM fulfillment_orders
GROUP BY warehouse_hub, carrier_name
ORDER BY total_refund_payout_usd DESC;

-- ------------------------------------------------------------------------------
-- QUERY 2: Pareto 80/20 Cumulative Distribution of Dispute Losses
-- Identifies the vital few routes causing the vast majority of financial loss
-- ------------------------------------------------------------------------------
WITH route_loss AS (
    SELECT 
        warehouse_hub || ' -> ' || carrier_name AS route_pair,
        SUM(refund_compensation_cost) AS route_payout_usd
    FROM fulfillment_orders
    GROUP BY warehouse_hub, carrier_name
),
ranked_routes AS (
    SELECT 
        route_pair,
        route_payout_usd,
        SUM(route_payout_usd) OVER () AS total_network_loss_usd,
        SUM(route_payout_usd) OVER (ORDER BY route_payout_usd DESC) AS running_loss_usd
    FROM route_loss
)
SELECT 
    route_pair,
    ROUND(route_payout_usd, 2) AS route_loss_usd,
    ROUND(running_loss_usd, 2) AS cumulative_loss_usd,
    ROUND((running_loss_usd * 100.0) / total_network_loss_usd, 2) AS cumulative_loss_pct,
    CASE 
        WHEN (running_loss_usd * 100.0) / total_network_loss_usd <= 80.0 THEN 'Vital Few (Focus Top Priority)'
        ELSE 'Useful Many'
    END AS pareto_classification
FROM ranked_routes
ORDER BY route_loss_usd DESC;
