# Business Process Flow Analysis: As-Is vs. To-Be Optimization
**Project:** Order-to-Delivery Process & SLA Bottleneck Optimization  
**Author:** Shivastha Rewaskar  

---

## 1. "As-Is" Workflow: Current High-Latency Process (31.95% Failure Rate)

In the current workflow, orders sit in unmonitored staging queues without SLA countdown tracking. Carrier allocation is static and static contracts favor low-cost but chronically delayed carriers like SwiftFreight.

```mermaid
flowchart TD
    Start(["Customer Places Order"]) --> Step1["ERP Ingestion & Batch Order Printing"]
    Step1 --> Step2["Warehouse Picking & Packing"]
    Step2 --> Bottleneck1{{"MANUAL STAGING QUEUE\n(No Real-Time Monitoring)\nAvg Delay: 27.8 hrs at Hub-North"}}
    
    Bottleneck1 --> Step3["Static Carrier Assignment\n(Default: SwiftFreight - 39.6% Breach)"]
    Step3 --> Step4["Carrier Handover & Transit"]
    
    Step4 --> CheckSLA{{"Delivery On Time?"}}
    CheckSLA -- "Yes (68%)" --> Success(["Order Delivered Successfully"])
    CheckSLA -- "No (32% Breach)" --> Bottleneck2["Customer Receives No Communication"]
    
    Bottleneck2 --> Step5["Customer Files Escalated Dispute"]
    Step5 --> Step6["Support Agent Manually Investigates Logs"]
    Step6 --> CostLoss(["$111K Direct Refund Payout Issued"])

    classDef danger fill:#fee2e2,stroke:#ef4444,stroke-width:2px;
    class Bottleneck1,Bottleneck2,CostLoss danger;
```

---

## 2. "To-Be" Workflow: Automated Dispatch Triage & Real-Time Rerouting (< 12% Target SLA)

The optimized future state implements automated threshold alerts at 16 hours, dynamic carrier allocation based on rolling performance, and proactive customer communication before disputes are filed.

```mermaid
flowchart TD
    Start(["Customer Places Order"]) --> Step1["Real-Time Order Ingestion API"]
    Step1 --> Step2["Automated Picking & Barcode Packing"]
    
    Step2 --> Monitor{{"Dynamic SLA Countdown Engine\nTime in Staging < 16h?"}}
    Monitor -- "Yes" --> RoutingEngine["Algorithmic Carrier Allocation Engine"]
    Monitor -- "No (>16h Staged)" --> Triage["AUTOMATED FLOOR ESCALATION\n- Visual Alert on Supervisor Dash\n- Priority Fast-Track Bay Assigned"]
    Triage --> RoutingEngine

    RoutingEngine --> CarrierCheck{{"Carrier 14-Day SLA Breach > 25%?"}}
    CarrierCheck -- "Yes (SwiftFreight Suppressed)" --> AltCarrier["Auto-Reroute to MetroLogistics / AeroExpress"]
    CarrierCheck -- "No" --> StdCarrier["Assign Primary Carrier"]
    
    AltCarrier --> Step3["Carrier Transit with Live Telemetry Webhooks"]
    StdCarrier --> Step3

    Step3 --> DelayMonitor{{"Transit Delay Detected (>12h)?"}}
    DelayMonitor -- "No" --> Delivered(["Delivered on Time (>88% Compliance)"])
    DelayMonitor -- "Yes" --> ProactiveCX["Automated Proactive SMS/Email to Customer\n+ $10 Goodwill Discount Voucher"]
    
    ProactiveCX --> Resolution(["Dispute Avoided & Brand NPS Preserved"])

    classDef success fill:#dcfce7,stroke:#22c55e,stroke-width:2px;
    class Delivered,Resolution,RoutingEngine success;
```

---

## 3. Gap Analysis Summary Table
| Process Phase | As-Is State (Current) | To-Be State (Optimized) | Business Impact |
| :--- | :--- | :--- | :--- |
| **Staging Queue** | Unmonitored batch queue; orders age 28h+ | Automated alert at 16 hours; supervisor priority queue | Reduces Hub-North dispatch latency by 42% |
| **Carrier Selection** | Hardcoded vendor assignment | Dynamic routing based on 14-day rolling reliability score | Suppresses underperforming carrier routes |
| **Delay Communication**| Silent until customer complains | Proactive notification sent before customer asks | Lowers dispute conversion from 49.6% to < 10% |
| **Carrier Accountability**| Manual end-of-year dispute review | Automated weekly penalty clawback ledger | Recovers up to $30K in vendor non-performance penalties |
