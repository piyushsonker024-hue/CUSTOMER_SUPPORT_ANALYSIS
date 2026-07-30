# Business Answers

**Candidate Name:** PIYUSH SONKER

**Date:** 30 July 2026

---

# Q1. Which category or region has the worst SLA breach rate, and what's actually driving it?

## Answer

After analyzing the dataset,Account Access has the highest SLA breach rate at 67.06%, making it the weakest-performing category.

Among all regions, the West region has the highest SLA breach rate at 66.63%.

To understand why this is happening, I compared SLA breach rates with average resolution times. Categories with longer average resolution times generally have higher SLA breach rates. This suggests that delayed ticket resolution is the primary driver of SLA failures. Possible reasons include higher ticket complexity, increased workload, or insufficient staffing.

### Calculation Used

- Created an SLA flag (`sla_breached == "Yes"`).
- Grouped tickets by Category.
- Calculated:

```
SLA Breach Rate =
(Breached Tickets / Total Tickets) × 100
```

- Repeated the same calculation for Region.
- Compared SLA breach rates with average resolution times.

---

# Q2. Is there a relationship between priority and resolution time? Which agent(s), if any, deviate from that pattern — and by how much?

## Answer

Yes.

There is a clear relationship between ticket priority and resolution time.

| Priority | Average Resolution Time |
|----------|------------------------:|
| Critical | 7.59 Hours |
| High | 26.45 Hours |
| Medium | 75.55 Hours |
| Low | 136.77 Hours |

This shows that higher-priority tickets are resolved much faster than lower-priority tickets, which is the expected operational behavior.

To identify unusual agent performance, I compared each agent's average resolution time with the overall average resolution time for the same priority level.

The largest deviation was observed for AGENT_07.

| Priority | Deviation |
|----------|----------:|
| Critical | +38.61 Hours |
| High | +136.17 Hours |
| Medium | +368.78 Hours |
| Low | +758.69 Hours |

This indicates that AGENT_07 consistently resolves tickets more slowly than expected and may require workload balancing or additional support.

### Calculation Used

1. Calculated average resolution time for each priority.
2. Calculated average resolution time for every Agent + Priority combination.
3. Computed:

```
Deviation =
Agent Average Resolution Time − Overall Priority Average
```

4. Ranked agents by highest positive deviation.

---

# Q3. Which customer(s) show frequent reopened tickets or low CSAT scores? Is that agent-driven, category-driven, or something else?

## Answer

Customers with the highest number of reopened tickets are:

| Customer | Reopened Tickets |
|----------|-----------------:|
| CUST_133 | 9 |
| CUST_084 | 9 |
| CUST_027 | 7 |
| CUST_057 | 7 |
| CUST_126 | 7 |

Customers with the lowest average CSAT scores are:

| Customer | Average CSAT |
|----------|-------------:|
| CUST_089 | 3.36 |
| CUST_037 | 3.50 |
| CUST_012 | 3.52 |
| CUST_027 | 3.57 |
| CUST_025 | 3.58 |

Rather than assuming these issues are customer-specific, I compared these customers with their assigned agents and ticket categories. This helps determine whether poor customer experience is caused by a particular support agent, recurring issue type, or operational bottlenecks.

### Calculation Used

Grouped tickets by customer and calculated:

- Total Tickets
- Average CSAT
- Number of Reopened Tickets

Then ranked customers by reopened tickets and average CSAT.

---

# Q4. Before trusting any of the above — what data quality issues did you find in this dataset, and how did you handle them?

## Answer

Before performing any analysis, I checked the dataset for common data quality issues.

| Data Quality Issue | Count | Action Taken |
|-------------------|------:|-------------|
| Missing Created Date | 73 | Converted to NaT |
| Missing Resolved Date | 1,040 | Left as missing because unresolved tickets are expected |
| Missing Resolution Time | 1,278 | Excluded from resolution-time calculations |
| Missing CSAT | 1,023 | Ignored while calculating average CSAT |
| Duplicate Ticket IDs | 15 | Removed duplicate records |
| Negative Resolution Time | 88 | Treated as invalid and excluded |

These cleaning steps ensured that the analysis was based on reliable and consistent data.

---

# Q5. If you could track exactly one metric weekly to catch support problems early, what would it be and why?

## Answer

I would recommend tracking the Weekly SLA Breach Rate.

This metric is the best early warning indicator because it reflects operational issues before they affect customer satisfaction.

An increase in SLA breaches usually indicates:

- Higher ticket backlog
- Slower resolution times
- Staffing shortages
- Process bottlenecks

Unlike CSAT, which measures customer feedback after service is completed, SLA Breach Rate provides an earlier signal that support performance is deteriorating.

Monitoring this KPI every week enables support managers to take corrective action before customer experience declines.

---

