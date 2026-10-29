"""
Verification script for Project 2 logistics SQL scripts.
"""
import sqlite3
import csv
import os

db = sqlite3.connect(":memory:")
cursor = db.cursor()

base_dir = os.path.dirname(os.path.abspath(__file__))
schema_file = os.path.join(base_dir, "sql", "01_logistics_schema_ddl.sql")
data_file = os.path.join(base_dir, "data", "orders_dispatch_logistics.csv")

with open(schema_file, "r") as f:
    cursor.executescript(f.read())

with open(data_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [(
        r["order_id"], r["customer_id"], r["order_timestamp"], r["warehouse_hub"],
        r["carrier_name"], r["dispatch_timestamp"], r["promised_delivery_timestamp"],
        r["actual_delivery_timestamp"], float(r["sla_target_hours"]), float(r["actual_turnaround_hours"]),
        float(r["dispatch_stage_hours"]), float(r["transit_stage_hours"]), int(r["is_sla_breach"]),
        float(r["breach_variance_hours"]), r["dispute_filed"], r["dispute_reason"],
        float(r["refund_compensation_cost"])
    ) for r in reader]

cursor.executemany("INSERT INTO fulfillment_orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
db.commit()
print(f"Project 2: Ingested {len(rows)} records successfully into SQLite.")

# Test script 2
with open(os.path.join(base_dir, "sql", "02_sla_breach_and_latency_analysis.sql"), "r") as f:
    for i, q in enumerate([q.strip() for q in f.read().split(";") if q.strip()], 1):
        cursor.execute(q)
        print(f"Latency Query {i} returned {len(cursor.fetchall())} rows.")

# Test script 3
with open(os.path.join(base_dir, "sql", "03_carrier_pareto_and_cost_impact.sql"), "r") as f:
    for i, q in enumerate([q.strip() for q in f.read().split(";") if q.strip()], 1):
        cursor.execute(q)
        print(f"Pareto Query {i} returned {len(cursor.fetchall())} rows.")

db.close()
print("All Project 2 SQL queries executed cleanly!")
