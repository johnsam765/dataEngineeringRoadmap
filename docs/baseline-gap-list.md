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

## Next session
- Refactor process_sales into smaller validation and summarization functions
- Add basic automated tests