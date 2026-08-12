# Retail Analysis Findings

## Executive Summary

This project uses a local retail transaction dataset to practice end-to-end applied analytics. The analysis focuses on revenue trends, product performance, regional contribution, customer value, and the relationship between discounts and revenue.

Because the dataset is an educational synthetic dataset, the findings demonstrate the analytical method rather than representing a real company's performance.

## Key Findings

### 1. Revenue trends

Revenue is summarized monthly to identify periods of stronger and weaker performance. The monthly trend chart provides a clear view of sales momentum and can be extended to include year-over-year comparisons when multiple years are available.

### 2. Product and category performance

Revenue is compared across categories and individual products. High-revenue products should be evaluated alongside unit volume so that expensive products are not mistaken for the strongest volume drivers.

### 3. Regional performance

Regional revenue and order counts reveal geographic concentration. A region with high revenue but relatively few orders may have a higher average order value, while a high-volume region may depend more on lower-priced products.

### 4. Customer value

Customer-level summaries rank customers by total spend, units purchased, and order count. These metrics are useful for identifying high-value customers and separating frequency from monetary value.

### 5. Discount and revenue relationship

The discount-versus-revenue scatterplot helps evaluate whether larger discounts are associated with larger transaction values. This relationship should be interpreted carefully because correlation does not establish that discounts caused higher revenue.

## Business Questions Answered

- Which periods generate the most revenue?
- Which categories and products contribute the most revenue?
- Which regions are the strongest contributors?
- Which customers generate the highest total spend?
- What patterns appear between discounts, quantity, and revenue?

## Recommendations

1. Track revenue and units together when evaluating product performance.
2. Monitor regional revenue alongside order counts and average order value.
3. Use customer-level rankings to support retention and loyalty analysis.
4. Evaluate discount campaigns using incremental revenue or margin rather than revenue alone.
5. Repeat the analysis on a larger real-world dataset with multiple years to identify seasonal and long-term trends.

## Limitations

- The dataset is synthetic and intentionally small.
- It does not contain product cost or profit margin, so profitability cannot be evaluated.
- It contains fewer customers and products than a production retail system.
- Causal claims should not be made from the descriptive analysis alone.
