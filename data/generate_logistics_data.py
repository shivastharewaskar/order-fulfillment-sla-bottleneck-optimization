"""
Order Fulfillment & Logistics Bottleneck Data Generator
Simulates realistic e-commerce logistics operations over 12 months.
Key dynamics:
- Multi-stage cycle time: Order -> Warehouse Dispatch -> Hub Handover -> Final Delivery
- Hub staging delay bottleneck (North Hub suffers severe dispatch latency)
- Carrier SLA performance variance (SpeedyLogistics vs SwiftFreight vs RegionalDirect)
- SLA breach driving customer dispute filings and refund costs
"""

import csv
import random
import datetime
import os

random.seed(101)

TOTAL_ORDERS = 8000
START_DATE = datetime.datetime(2025, 1, 1, 8, 0, 0)
END_DATE = datetime.datetime(2025, 12, 31, 20, 0, 0)

HUBS = {
    "HUB-NORTH": {"dispatch_delay_prob": 0.38, "avg_dispatch_hrs": 34.0},
    "HUB-SOUTH": {"dispatch_delay_prob": 0.12, "avg_dispatch_hrs": 14.0},
    "HUB-EAST": {"dispatch_delay_prob": 0.16, "avg_dispatch_hrs": 18.0},
    "HUB-WEST": {"dispatch_delay_prob": 0.10, "avg_dispatch_hrs": 12.0}
}

CARRIERS = {
    "SwiftFreight": {"transit_fail_prob": 0.28, "sla_hours": 72},
    "MetroLogistics": {"transit_fail_prob": 0.12, "sla_hours": 48},
    "AeroExpress": {"transit_fail_prob": 0.05, "sla_hours": 24},
    "RegionalPost": {"transit_fail_prob": 0.19, "sla_hours": 96}
}

DISPUTE_REASONS = [
    "Late Delivery / Missed Event Deadline",
    "Damaged Goods During Delayed Transit",
    "Incorrect Tracking / In-Transit Blackout",
    "Missing Items from Incomplete Package",
    "Wrong Delivery Address Attempt"
]

def generate_records():
    records = []
    
    delta_seconds = int((END_DATE - START_DATE).total_seconds())
    
    for order_num in range(10001, 10001 + TOTAL_ORDERS):
        order_sec = random.randint(0, delta_seconds)
        order_time = START_DATE + datetime.timedelta(seconds=order_sec)
        
        hub_name = random.choices(list(HUBS.keys()), weights=[0.40, 0.25, 0.20, 0.15])[0]
        carrier_name = random.choices(list(CARRIERS.keys()), weights=[0.35, 0.30, 0.15, 0.20])[0]
        
        hub_info = HUBS[hub_name]
        carrier_info = CARRIERS[carrier_name]
        
        # 1. Warehouse Dispatch Stage
        has_warehouse_delay = random.random() < hub_info["dispatch_delay_prob"]
        if has_warehouse_delay:
            dispatch_hours = random.uniform(28.0, 72.0)
        else:
            dispatch_hours = random.uniform(6.0, 24.0)
            
        dispatch_time = order_time + datetime.timedelta(hours=dispatch_hours)
        
        # 2. Transit Stage
        sla_transit_target_hours = carrier_info["sla_hours"]
        has_transit_delay = random.random() < carrier_info["transit_fail_prob"]
        
        if has_transit_delay:
            transit_hours = sla_transit_target_hours * random.uniform(1.25, 2.2)
        else:
            transit_hours = sla_transit_target_hours * random.uniform(0.6, 0.95)
            
        actual_delivery_time = dispatch_time + datetime.timedelta(hours=transit_hours)
        
        # Promised SLA from order timestamp:
        # Standard SLA is 24h dispatch + carrier SLA
        total_sla_allowed_hours = 24.0 + sla_transit_target_hours
        promised_delivery_time = order_time + datetime.timedelta(hours=total_sla_allowed_hours)
        
        # Total actual turnaround time (TAT)
        total_actual_hours = (actual_delivery_time - order_time).total_seconds() / 3600.0
        
        is_sla_breach = total_actual_hours > total_sla_allowed_hours
        variance_hours = round(total_actual_hours - total_sla_allowed_hours, 2)
        
        # Customer dispute likelihood
        dispute_filed = "No"
        dispute_reason = "None"
        refund_amount = 0.00
        
        if is_sla_breach:
            # The worse the delay, the higher the dispute filing
            dispute_prob = 0.25 if variance_hours < 24 else (0.55 if variance_hours < 48 else 0.85)
            if random.random() < dispute_prob:
                dispute_filed = "Yes"
                dispute_reason = "Late Delivery / Missed Event Deadline" if random.random() < 0.70 else random.choice(DISPUTE_REASONS)
                refund_amount = round(random.uniform(25.0, 150.0), 2)
                
        records.append({
            "order_id": f"ORD-{order_num}",
            "customer_id": f"CUST-{random.randint(5000, 9999)}",
            "order_timestamp": order_time.strftime("%Y-%m-%d %H:%M:%S"),
            "warehouse_hub": hub_name,
            "carrier_name": carrier_name,
            "dispatch_timestamp": dispatch_time.strftime("%Y-%m-%d %H:%M:%S"),
            "promised_delivery_timestamp": promised_delivery_time.strftime("%Y-%m-%d %H:%M:%S"),
            "actual_delivery_timestamp": actual_delivery_time.strftime("%Y-%m-%d %H:%M:%S"),
            "sla_target_hours": round(total_sla_allowed_hours, 1),
            "actual_turnaround_hours": round(total_actual_hours, 1),
            "dispatch_stage_hours": round(dispatch_hours, 1),
            "transit_stage_hours": round(transit_hours, 1),
            "is_sla_breach": 1 if is_sla_breach else 0,
            "breach_variance_hours": variance_hours if variance_hours > 0 else 0.0,
            "dispute_filed": dispute_filed,
            "dispute_reason": dispute_reason,
            "refund_compensation_cost": refund_amount
        })
        
    return records

def save_csv():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(output_dir, "orders_dispatch_logistics.csv")
    
    records = generate_records()
    fieldnames = list(records[0].keys())
    
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Generated {len(records)} logistics records at {file_path}")

if __name__ == "__main__":
    save_csv()
