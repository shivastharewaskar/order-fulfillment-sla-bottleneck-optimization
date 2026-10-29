-- ==============================================================================
-- PROJECT 2: Order-to-Delivery Process & SLA Bottleneck Optimization
-- SCRIPT: 01_logistics_schema_ddl.sql
-- DESCRIPTION: Schema definition and indexing for multi-stage logistics tracking
-- AUTHOR: Shivastha Rewaskar
-- ==============================================================================

DROP TABLE IF EXISTS fulfillment_orders;

CREATE TABLE fulfillment_orders (
    order_id                     VARCHAR(20) PRIMARY KEY,
    customer_id                  VARCHAR(20) NOT NULL,
    order_timestamp              TIMESTAMP NOT NULL,
    warehouse_hub                VARCHAR(30) NOT NULL,
    carrier_name                 VARCHAR(50) NOT NULL,
    dispatch_timestamp           TIMESTAMP NOT NULL,
    promised_delivery_timestamp  TIMESTAMP NOT NULL,
    actual_delivery_timestamp    TIMESTAMP NOT NULL,
    sla_target_hours             DECIMAL(6, 1) NOT NULL,
    actual_turnaround_hours      DECIMAL(6, 1) NOT NULL,
    dispatch_stage_hours         DECIMAL(6, 1) NOT NULL,
    transit_stage_hours          DECIMAL(6, 1) NOT NULL,
    is_sla_breach                INTEGER CHECK (is_sla_breach IN (0, 1)),
    breach_variance_hours        DECIMAL(6, 1) DEFAULT 0.0,
    dispute_filed                VARCHAR(5) NOT NULL, -- Yes, No
    dispute_reason               VARCHAR(150),
    refund_compensation_cost     DECIMAL(10, 2) DEFAULT 0.00
);

-- Analytics & Performance Indexes
CREATE INDEX idx_hub ON fulfillment_orders (warehouse_hub);
CREATE INDEX idx_carrier ON fulfillment_orders (carrier_name);
CREATE INDEX idx_breach ON fulfillment_orders (is_sla_breach);
CREATE INDEX idx_order_time ON fulfillment_orders (order_timestamp);
