-- =====================================================
-- ADVANCED SQL EXERCISES
-- Python + SQL Data Engineering Mastery
-- Updated: October 20, 2026
--
-- Focus:
-- CTEs, grain, joins, aggregation, reconciliation,
-- deduplication, window functions and null handling
-- =====================================================


-- =====================================================
-- EXERCISE 1: PAYMENT RECONCILIATION
-- =====================================================
-- Business requirement:
-- Return every sale, including sales without payments.
--
-- Output grain: One row per sale_id.
--
-- Key learning:
-- Aggregate payments before joining to avoid fan-out.
-- =====================================================

WITH payment_summary AS (
    SELECT
        sale_id,
        COUNT(*) AS payment_count,
        SUM(payment_amount) AS total_paid
    FROM payments
    GROUP BY sale_id
)
SELECT
    s.sale_id,
    s.amount AS sale_amount,
    COALESCE(ps.payment_count, 0) AS payment_count,
    COALESCE(ps.total_paid, 0) AS total_paid,
    s.amount - COALESCE(ps.total_paid, 0)
        AS outstanding_amount
FROM sales s
LEFT JOIN payment_summary ps
    ON s.sale_id = ps.sale_id
ORDER BY s.sale_id;


-- =====================================================
-- EXERCISE 2: LATEST-RECORD DEDUPLICATION
-- =====================================================
-- Business requirement:
-- Keep only the latest version of each sale.
--
-- Output grain: One row per sale_id.
--
-- Key learning:
-- ROW_NUMBER, PARTITION BY, ordering and tie-breakers.
--
-- Assumption:
-- source_version increases with each source update.
-- =====================================================

WITH ranked_sales AS (
    SELECT
        sale_id,
        amount,
        status,
        updated_at,
        source_version,
        ROW_NUMBER() OVER (
            PARTITION BY sale_id
            ORDER BY
                updated_at DESC,
                source_version DESC
        ) AS rn
    FROM sales_history
)
SELECT
    sale_id,
    amount,
    status,
    updated_at,
    source_version
FROM ranked_sales
WHERE rn = 1
ORDER BY sale_id;


-- =====================================================
-- EXERCISE 3: REGIONAL FINANCIAL RECONCILIATION
-- =====================================================
-- Business requirement:
-- Calculate completed sales, sales totals, payments
-- received and outstanding amounts by region.
--
-- Output grain: One row per region.
--
-- Key learning:
-- CTE pre-aggregation, LEFT JOIN, GROUP BY,
-- COALESCE and correct status filtering.
--
-- Assumptions:
-- sales has one row per sale_id.
-- Completed sale amounts have passed quality checks.
-- =====================================================

WITH payment_summary AS (
    SELECT
        sale_id,
        SUM(payment_amount) AS total_paid
    FROM payments
    GROUP BY sale_id
)
SELECT
    s.region,
    COUNT(*) AS completed_sales,
    SUM(s.amount) AS sales_total,
    SUM(COALESCE(ps.total_paid, 0))
        AS payment_total,
    SUM(s.amount)
        - SUM(COALESCE(ps.total_paid, 0))
        AS outstanding_total
FROM sales s
LEFT JOIN payment_summary ps
    ON s.sale_id = ps.sale_id
WHERE s.status = 'Completed'
GROUP BY s.region
ORDER BY s.region;