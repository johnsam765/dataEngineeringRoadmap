SELECT
    region,
    COUNT(
        CASE
            WHEN status = 'Completed' THEN 1
        END
    ) AS completed_order_count,
    COUNT(
        CASE
            WHEN status = 'Cancelled' THEN 1
        END
    ) AS cancelled_order_count,
    SUM(
        CASE
            WHEN status = 'Completed'
                 AND amount IS NOT NULL
            THEN amount
            ELSE 0
        END
    ) AS completed_sales_amount
FROM sales_raw
WHERE region IS NOT NULL
GROUP BY region
HAVING COUNT(
    CASE
        WHEN status = 'Completed' THEN 1
    END
) >= 2
ORDER BY completed_sales_amount DESC;

-- -------------------------------------------------
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(sr.sale_id) AS total_order_count,
    SUM(
        CASE
            WHEN sr.status = 'Completed' THEN 1
            ELSE 0
        END
    ) AS completed_order_count,
    SUM(
        CASE
            WHEN sr.status = 'Completed'
                THEN COALESCE(sr.amount, 0)
            ELSE 0
        END
    ) AS completed_sales_amount
FROM customers AS c
LEFT JOIN sales_raw AS sr
    ON c.customer_id = sr.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY
    completed_sales_amount DESC,
    c.customer_id ASC;
-- --------------------------------------------------
WITH latest_data AS (
    SELECT
        sr.sale_id,
        sr.customer_id,
        sr.region,
        sr.amount,
        sr.status,
        sr.updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY sr.sale_id
            ORDER BY sr.updated_at DESC
        ) AS rn
    FROM sales_raw AS sr
)
SELECT
    sale_id,
    customer_id,
    region,
    amount,
    status,
    updated_at
FROM latest_data
WHERE rn = 1;