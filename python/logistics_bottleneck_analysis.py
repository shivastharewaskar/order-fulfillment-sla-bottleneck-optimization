"""
Project 2: Order Fulfillment SLA & Bottleneck Optimization
Script: logistics_bottleneck_analysis.py
Performs end-to-end logistics operations analysis, multi-stage turnaround latency calculations,
carrier reliability metrics, and dispute financial loss quantification.
"""

import csv
import os
from collections import defaultdict

def run_logistics_analysis():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "orders_dispatch_logistics.csv")
    
    total_orders = 0
    total_breaches = 0
    total_disputes = 0
    total_refund_payout = 0.0
    
    hub_data = defaultdict(lambda: {"orders": 0, "breaches": 0, "dispatch_hours_sum": 0.0, "disputes": 0, "refunds": 0.0})
    carrier_data = defaultdict(lambda: {"orders": 0, "breaches": 0, "transit_hours_sum": 0.0, "disputes": 0, "refunds": 0.0})
    dispute_reasons = defaultdict(int)
    
    with open(data_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_orders += 1
            hub = row["warehouse_hub"]
            carrier = row["carrier_name"]
            is_breach = int(row["is_sla_breach"])
            dispute = row["dispute_filed"] == "Yes"
            refund = float(row["refund_compensation_cost"])
            dispatch_hrs = float(row["dispatch_stage_hours"])
            transit_hrs = float(row["transit_stage_hours"])
            
            if is_breach:
                total_breaches += 1
            if dispute:
                total_disputes += 1
                total_refund_payout += refund
                dispute_reasons[row["dispute_reason"]] += 1
                
            hub_data[hub]["orders"] += 1
            hub_data[hub]["breaches"] += is_breach
            hub_data[hub]["dispatch_hours_sum"] += dispatch_hrs
            hub_data[hub]["disputes"] += 1 if dispute else 0
            hub_data[hub]["refunds"] += refund
            
            carrier_data[carrier]["orders"] += 1
            carrier_data[carrier]["breaches"] += is_breach
            carrier_data[carrier]["transit_hours_sum"] += transit_hrs
            carrier_data[carrier]["disputes"] += 1 if dispute else 0
            carrier_data[carrier]["refunds"] += refund
            
    overall_breach_rate = (total_breaches / total_orders) * 100
    breach_to_dispute_rate = (total_disputes / total_breaches) * 100 if total_breaches > 0 else 0
    
    print("=" * 85)
    print("       LOGISTICS OPERATIONS & SLA BOTTLENECK AUDIT - EXECUTIVE REPORT       ")
    print("=" * 85)
    print(f"Total Fulfillment Consignments: {total_orders:,}")
    print(f"Total SLA Target Breaches:     {total_breaches:,} ({overall_breach_rate:.2f}%)")
    print(f"Customer Disputes Escalated:    {total_disputes:,} ({breach_to_dispute_rate:.2f}% of breaches)")
    print(f"Total Direct Refund Payouts:    ${total_refund_payout:,.2f}")
    print("-" * 85)
    
    print("\n1. WAREHOUSE STAGING BOTTLENECKS (DISPATCH LATENCY)")
    print(f"{'Hub Name':<15} | {'Total Orders':<12} | {'Breaches':<10} | {'Breach Rate %':<14} | {'Avg Dispatch (h)':<18}")
    print("-" * 85)
    for hub, s in sorted(hub_data.items(), key=lambda x: (x[1]["breaches"] / x[1]["orders"]), reverse=True):
        b_rate = (s["breaches"] / s["orders"]) * 100
        avg_disp = s["dispatch_hours_sum"] / s["orders"]
        print(f"{hub:<15} | {s['orders']:<12} | {s['breaches']:<10} | {b_rate:<13.2f}% | {avg_disp:<17.1f}h")
        
    print("\n2. CARRIER TRANSIT RELIABILITY & FINANCIAL DISPUTE EXPOSURE")
    print(f"{'Carrier Name':<18} | {'Orders':<8} | {'Breaches':<10} | {'Breach %':<10} | {'Disputes':<10} | {'Refund Loss ($)':<15}")
    print("-" * 85)
    for c, s in sorted(carrier_data.items(), key=lambda x: s["refunds"], reverse=True):
        b_rate = (s["breaches"] / s["orders"]) * 100
        print(f"{c:<18} | {s['orders']:<8} | {s['breaches']:<10} | {b_rate:<9.2f}% | {s['disputes']:<10} | ${s['refunds']:<14,.2f}")
        
    print("\n3. PRIMARY DISPUTE CATEGORIES")
    print(f"{'Reason':<45} | {'Count':<8} | {'% of All Disputes':<15}")
    print("-" * 85)
    for r, count in sorted(dispute_reasons.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_disputes) * 100 if total_disputes > 0 else 0
        print(f"{r:<45} | {count:<8} | {pct:<14.2f}%")
    print("=" * 85)

if __name__ == "__main__":
    run_logistics_analysis()
