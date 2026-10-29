-- ==============================================================================
-- PROJECT 2: Order-to-Delivery Process & SLA Bottleneck Optimization
-- SCRIPT: 02_sla_breach_and_latency_analysis.sql
-- DESCRIPTION: Multi-stage latency breakdown isolating warehouse vs transit delay
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Warehouse Hub Staging Efficiency vs. SLA Failure Rate
-- Identifies internal warehouse bottlenecks (Target dispatch SLA: 24.0 hours)
-- ------------------------------------------------------------------------------
SELECT 
    warehouse_hub,
    COUNT(order_id) AS total_orders,
    ROUND(AVG(dispatch_stage_hours), 2) AS avg_warehouse_dispatch_hours,
    ROUND(MAX(dispatch_stage_hours), 2) AS max_warehouse_dispatch_hours,
    SUM(CASE WHEN dispatch_stage_hours > 24.0 THEN 1 ELSE 0 END) AS internal_dispatch_breaches,
    ROUND(SUM(CASE WHEN dispatch_stage_hours > 24.0 THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(order_id), 2) AS internal_breach_rate_pct,
    SUM(is_sla_breach) AS total_customer_sla_breaches,
    ROUND(SUM(is_sla_breach) * 100.0 / COUNT(order_id), 2) AS total_breach_rate_pct
FROM fulfillment_orders
GROUP BY warehouse_hub
ORDER BY total_breach_rate_pct DESC;

-- ------------------------------------------------------------------------------
-- QUERY 2: Carrier Transit Reliability Matrix
-- Compares promised transit commitments vs actual execution
-- ------------------------------------------------------------------------------
SELECT 
    carrier_name,
    COUNT(order_id) AS total_consignments,
    ROUND(AVG(sla_target_hours), 1) AS avg_target_sla_hrs,
    ROUND(AVG(transit_stage_hours), 1) AS avg_actual_transit_hrs,
    SUM(is_sla_breach) AS total_breached_deliveries,
    ROUND(SUM(is_sla_breach) * 100.0 / COUNT(order_id), 2) AS carrier_breach_rate_pct,
    ROUND(AVG(CASE WHEN is_sla_breach = 1 THEN breach_variance_hours ELSE NULL END), 1) AS avg_delay_severity_hrs
FROM fulfillment_orders
GROUP BY carrier_name
ORDER BY carrier_breach_rate_pct DESC;

-- ------------------------------------------------------------------------------
-- QUERY 3: Multi-Stage Root Cause Attribution (Warehouse vs. Carrier Fault)
-- Classifies whether late orders failed at Dispatch or during Last-Mile Transit
-- ------------------------------------------------------------------------------
WITH delay_attribution AS (
    SELECT 
        order_id,
        warehouse_hub,
        carrier_name,
        dispatch_stage_hours,
        transit_stage_hours,
        breach_variance_hours,
        CASE 
            WHEN dispatch_stage_hours > 24.0 AND breach_variance_hours > 0 AND (transit_stage_hours <= sla_target_hours - 24.0) 
                 THEN 'Warehouse Dispatch Bottleneck Solely'
            WHEN dispatch_stage_hours <= 24.0 AND breach_variance_hours > 0 
                 THEN 'Carrier Transit Delay Solely'
            WHEN dispatch_stage_hours > 24.0 AND breach_variance_hours > 0 
                 THEN 'Compound Failure (Warehouse + Carrier)'
            ELSE 'Delivered Within SLA'
        END AS primary_delay_attribution
    FROM fulfillment_orders
    WHERE is_sla_breach = 1
)
SELECT 
    primary_delay_attribution,
    COUNT(order_id) AS breach_count,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM fulfillment_orders WHERE is_sla_breach = 1), 2) AS pct_of_all_breaches
FROM delay_attribution
GROUP BY primary_delay_attribution
ORDER BY breach_count DESC;
