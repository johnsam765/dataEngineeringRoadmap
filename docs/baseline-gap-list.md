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

## August 5th, 2026 — Session 3
Current test status:
- 5 tests passed

Completed:
- Tested valid completed sales
- Tested cancelled sales
- Tested duplicate rejection
- Tested missing-key handling
- Verified process_sales uses supplied records rather than global data

## August 6, 2026

Completed:
- Closed-book rebuild of sales validation/processing logic
- SQL Exercises 4–7
- Practised LEFT JOIN filter placement
- Practised customer/region grain
- Practised HAVING with multiple conditions
- Practised ROW_NUMBER deduplication before aggregation

SQL progress:
- 7 of 15 exercises completed

Key mistakes/learning:
- RIGHT-table filters in WHERE can remove unmatched LEFT JOIN rows
- COUNT(COALESCE(column, 0)) is wrong for counting actual matches
- GROUP BY should follow the intended output grain
- Latest-record ROW_NUMBER requires ORDER BY updated_at DESC

Next starting point:
- SQL Exercise 8: deduplicate sales first, then join to customers while preserving one row per customer

## August 12, 2026 — Sessions 4–5

Completed:

- Finished SQL Exercises 8–15
- Completed the full 15/15 SQL joins and aggregation exercise set
- Practised join fan-out / row multiplication
- Practised pre-aggregating child records before joins
- Practised moving between payment, sale, and customer grain
- Practised COUNT versus COUNT(DISTINCT)
- Practised conditional aggregation with joins and HAVING
- Completed 5/5 SQL window-function exercises
- Practised RANK, LAG, LEAD, and running SUM
- Combined multiple window functions in the same query

SQL progress:

- 15 of 15 join/grouping exercises completed
- 5 of 5 window-function exercises completed

Key SQL learning:

- Always identify what one row represents before joining or grouping
- A one-to-many join can change the output grain and repeat measures
- Pre-aggregate the many-side when necessary before joining
- GROUP BY changes grain; window functions generally preserve grain
- COUNT(value) counts non-null rows
- SUM(value) adds the values already present in those rows
- COUNT(DISTINCT key) can protect logical entity counts after fan-out
- PARTITION BY defines where a window calculation restarts
- ORDER BY inside a window defines ranking, previous/next, or running-total order
- The window ORDER BY must match the business meaning, such as time versus amount

Areas to continue reviewing:

- Identifying the correct grain quickly before writing a query
- Recognizing when a measure will be duplicated by a join
- Deciding when to pre-aggregate before joining
- Remembering that including a lower-grain key such as sale_id in GROUP BY keeps the result at that lower grain

## August 12, 2026 — Python Exceptions, Logging, and Testing

Completed:

- Added run_batch as the batch-level controller
- Added batch input validation
- Added ValueError when records is None
- Practised try/except
- Practised re-raising exceptions after logging
- Added INFO logging for batch start and completion
- Added WARNING logging for rejected records
- Added ERROR logging for batch-level failures
- Added accepted/rejected record counts to the completion log
- Added pytest test for ValueError
- Tested the exception message using pytest.raises(..., match=...)
- Added log testing using the pytest caplog fixture
- Tested the batch completion summary log

Current test status:

- 8 tests passed

Key Python learning:

- Bad individual records are rejected and processing can continue
- Invalid batch-level input can raise an exception and fail the batch
- Catching an exception does not mean it should be swallowed
- Log useful failure context and re-raise when the batch must remain failed
- Keep validation responsible for determining what is wrong
- Handle logging/rejection behaviour in the processing/controller layer
- INFO is for normal pipeline lifecycle events
- WARNING is for recoverable record-level problems
- ERROR is for batch-level failures
- caplog.text contains the log output captured by pytest during a test

Next starting point:

- Begin the next roadmap section with a short closed-book review
- Rebuild the important grain/fan-out concepts without hints
- Review exceptions and logging briefly
- Continue to the next planned data engineering topic rather than adding more exercises to the completed block