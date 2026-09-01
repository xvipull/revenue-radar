# Product charter

## Objective
Detect pricing, discount, return, and margin exceptions early enough for Finance and Sales Operations to recover value and prevent repeat leakage.

## Stakeholders and decisions
| Persona | Decision enabled |
|---|---|
| CFO | Prioritise recovery actions and assess margin-bridge drivers. |
| Sales Operations | Approve, reverse, or coach on discount exceptions. |
| Finance Controller | Reconcile revenue, verify controls, and close exceptions. |

## Scope
In scope: invoiced orders, list prices, approved-discount policy, returns, customer/product profitability, and daily exception queues. Out of scope: cash collection, tax filing, and journal posting.

## Operating assumptions
Daily refresh by 07:00 local time; USD reporting currency; a discount above the product policy is an exception unless explicitly approved. Finance owns reconciliation; Sales Ops owns remediation.

## Acceptance criteria
1. Every reporting order resolves to a product and customer master record.
2. Curated net revenue reconciles to source orders less returns within $0.01.
3. Required-field failures, duplicates, range failures, and referential failures are reported.
4. Exception queue explains the flag and estimated recoverable value for every scored order.

## Security and risk
Use least-privilege roles and customer identifiers only; exclude payment data and PII beyond business contact attributes. Synthetic data is supplied for this portfolio build. Risk: policy thresholds may create false positives; Finance validates decisions before recovery.

