# Business Requirements Document (BRD)
## Project: Automated Order Staging Triage & Real-Time Carrier SLA Optimization
**Document Reference:** BRD-OPS-2026-004  
**Author:** Shivastha Rewaskar (Lead Business & Systems Analyst)  
**Version:** 1.0 (Final Approved)  
**Status:** Ready for Engineering Implementation  

---

### 1. Project Background & Executive Summary
The organization processes over 8,000 monthly e-commerce consignments across four fulfillment hubs. In 2025, the order fulfillment network experienced an aggregate **31.95% SLA breach rate**, resulting in **1,269 escalated customer dispute tickets** and **$111,475.47 in direct refund compensation payouts**.

Operational audit revealed that **HUB-NORTH** generates 40.95% SLA failure due to manual dispatch staging bottlenecks (averaging 27.8 hours against a 24.0-hour internal benchmark), while carrier **SwiftFreight** alone accounts for **48.6% of all network refund payouts ($54.2K)**.

This project specifies requirements for an **Automated Order Staging Triage System (AOSTS)** and dynamic carrier allocation engine to reduce network SLA breaches below **12.0%** and cut compensation payouts by **65%**.

---

### 2. Stakeholder Register
| Stakeholder Role | Department | Key Interest / Responsibility |
| :--- | :--- | :--- |
| **VP of Supply Chain & Logistics** | Operations | Overall network fulfillment speed, SLA compliance, cost per order |
| **Warehouse Operations Managers** | Fulfillment Hubs | Staging queue visibility, pick-and-pack workflow balancing |
| **Head of Customer Experience** | Support / CX | Reduction in customer delivery complaints, WISMO (Where Is My Order) tickets |
| **Carrier Relations Manager** | Procurement | Carrier contract negotiations, penalty clawbacks, transit monitoring |
| **Lead Systems Engineer** | IT / Software | ERP/WMS API integration, real-time dispatch queue architecture |

---

### 3. Business Objectives & Success Metrics (SMART)
1. **Reduce Aggregate SLA Breach Rate:** Decrease network delivery breaches from **31.95% to < 12.0%** within 6 months of rollout.
2. **Eliminate Hub-North Dispatch Latency:** Decrease average warehouse staging time at HUB-NORTH from **27.8 hours to < 16.0 hours**.
3. **Mitigate Financial Compensation Losses:** Reduce annual dispute refund compensation payouts by **$72,000+**.
4. **Automate Carrier Rerouting:** Automatically suppress carriers whose 14-day rolling breach rate exceeds 25% from receiving high-priority orders.

---

### 4. Functional Requirements (FR)

| Req ID | Requirement Title | Description & Acceptance Criteria | Priority |
| :--- | :--- | :--- | :---: |
| **FR-01** | **Automated Staging Alert** | The WMS shall trigger a warning alert on warehouse floor monitors when an order has remained in "Pack & Stage" status for **> 16 hours**. Acceptance: Audible/visual alert displayed on dashboard. | Must Have |
| **FR-02** | **Dynamic Carrier Scoring** | The system shall compute a 14-day rolling transit reliability score for each carrier-hub route. If a carrier's breach rate exceeds 25%, the system shall demote the carrier to secondary priority. | Must Have |
| **FR-03** | **Proactive Delay Messaging** | When actual dispatch latency exceeds 24 hours, an automated SMS/Email notification shall be dispatched to the customer with an updated expected delivery window. | Should Have |
| **FR-04** | **Carrier Penalty Audit Log** | The system shall generate a monthly automated report detailing verified transit delays exceeding contracted SLA terms for vendor invoice clawback reconciliation. | Must Have |
| **FR-05** | **Capacity-Based Order Routing** | If HUB-NORTH queue volume exceeds 85% capacity, incoming orders from overlapping postal zones shall automatically reroute to HUB-EAST. | Could Have |

---

### 5. Non-Functional Requirements (NFR)
* **NFR-01 (Performance & Latency):** Carrier allocation engine must process and assign shipping labels within **1.5 seconds** of order packing confirmation.
* **NFR-02 (Availability):** Staging alert monitor service must maintain **99.95% uptime** during operational fulfillment hours.
* **NFR-03 (Security):** Customer addresses and delivery logs must comply with SOC-2 and data encryption at rest (AES-256).

---

### 6. User Stories & Acceptance Criteria

#### User Story 1 (Warehouse Dispatch Supervisor)
> *As a Warehouse Operations Supervisor at HUB-NORTH, I want a real-time monitor highlighting orders approaching their 24-hour dispatch deadline, so that my floor team can prioritize staging high-risk shipments before SLA breach.*
* **Acceptance Criteria:**
  - Orders between 16–20 hours appear highlighted in Yellow.
  - Orders > 20 hours appear highlighted in Blinking Red with an emergency pick order generated.

#### User Story 2 (Customer Support Specialist)
> *As a Customer Support Agent, I want the system to automatically tag orders experiencing compound carrier delays, so that I can issue customer goodwill vouchers before the customer files an escalated dispute.*
* **Acceptance Criteria:**
  - Automated ticket creation in Zendesk/Freshdesk when carrier tracking reports > 24 hours delay.
