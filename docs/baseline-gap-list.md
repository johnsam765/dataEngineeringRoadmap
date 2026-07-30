# Baseline Assessment — July 28, 2026

## SQL

Confident:
- Conditional aggregation
- GROUP BY and HAVING
- Null handling in aggregates
- ROW_NUMBER deduplication

Weak:
- Preserving grain after joins
- COUNT(*) versus COUNT(column) with LEFT JOIN

Errors made:
- Counted the LEFT JOIN placeholder row
- Initially grouped by an unnecessary region column
- Initially sorted by the wrong measure

## Python

Confident:
- Loops and conditions
- Dictionaries and lists
- Sets for duplicate detection
- Record validation
- Regional aggregation

Weak:
- Avoiding global variables inside functions
- Defensive handling of missing dictionary keys
- Separating accepted records from aggregation-eligible records

Errors made:
- Used the global sales variable instead of the records parameter
- Initially counted cancelled records in the completed summary
- Initially used a list instead of a set for duplicate detection

## Baseline follow-up
Completed:
- Refactored process_sales into validation, summarization, and controller functions
- Added initial automated tests

## July 29, 2026 — Session 2

Completed:
- Created a Windows virtual environment for the repository
- Installed pytest
- Split sales processing into validation, summarization, and controller functions
- Added rejection reasons to invalid records
- Added tests for completed, cancelled, and duplicate sales

Current test status:
- 3 tests passed

Still to complete:
- Test missing sale_id key handling
- Test that process_sales uses only the supplied records
- Review and clean type hints and formatting

Next starting point:
- Open tests/test_sales_baseline.py
- Add test_missing_sale_id_key_is_rejected_without_error