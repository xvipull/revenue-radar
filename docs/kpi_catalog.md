# KPI catalog

| KPI | Definition | Grain / owner |
|---|---|---|
| Net revenue | invoiced gross less discount less returns | order line / Finance |
| Gross margin % | `(net revenue - COGS) / net revenue` | order line / Finance |
| Leakage value | price shortfall plus unapproved discount value plus return value, capped at order gross | order line / Finance |
| Price variance | `(list price - invoiced unit price) × quantity`, floor at zero | order line / Sales Ops |
| Return rate | return value ÷ invoiced gross | order line / Sales Ops |
| Unreconciled count | order lines with unresolved master data or failed balance | order line / Controller |

Values are USD. Negative revenue is retained only where it is an explicit return; all rounding occurs at reporting output, not the curated layer.

