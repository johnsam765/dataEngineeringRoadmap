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

## October 15, 2026 — Python Ingestion, Serialization, and Data Quality

**Completed:**
- Implemented CSV ingestion using `csv.DictReader` and `pathlib`
- Implemented numeric normalization (`str` → `int` / `float`, empty values → `None`)
- Created reusable `normalize_records()` function
- Added record-level `try/except` handling for invalid numeric values
- Preserved original source records using `.copy()`
- Implemented rejection handling without stopping valid records from processing
- Implemented reusable JSON output writer using `json.dump()`
- Persisted accepted and rejected records into separate JSON files
- Added ingestion, normalization, JSON-writing, and malformed-record recovery tests

**Current test status:**
- **14 tests passed**

**Key Python learning:**
- `tmp_path` creates isolated temporary directories for pytest
- `pytest.raises()` verifies expected exceptions
- `isinstance()` checks data types; `is None` checks null values
- Dictionaries are mutable; `.copy()` prevents modification of the original flat record
- `try/except` enables record-level recovery when appropriate
- Rejected records should preserve the original input and rejection reason
- `json.dump()` serializes Python data to a file
- `json.load()` / `json.loads()` deserialize JSON data
- A reusable function should be separate from the `__main__` execution block

**Areas to improve:**
- Distinguish `INVALID_AMOUNT` from `INVALID_SALE_ID`
- Handle missing keys and malformed CSV structures
- Add automated end-to-end pipeline tests
- Integrate `run_batch()` consistently into the execution flow
- Verify reconciliation across accepted and rejected records
- Improve logging for normalization failures

**Next starting point:**
- Continue advanced SQL exercises: CTEs, join grain, fan-out, aggregation, and reconciliation
- Later integrate Python ingestion with relational database loading

## October 20, 2026 — Advanced SQL and Production Python Error Handling

### SQL — Completed

- Completed three additional production-style SQL exercises.
- Implemented payment reconciliation using CTEs and pre-aggregation.
- Practised `LEFT JOIN`, `COALESCE`, `COUNT`, `SUM`, and outstanding-balance calculations.
- Implemented latest-record deduplication using `ROW_NUMBER()`.
- Handled duplicate timestamps using a source-version tie-breaker.
- Implemented regional financial reconciliation with Completed sales only.
- Practised preserving the intended grain across payment, sale, and region levels.

### SQL — Key Learning

- Determine the target output grain before writing joins or aggregations.
- Pre-aggregate child tables when joining detailed rows would incorrectly multiply measures.
- `ORDER BY updated_at DESC` selects the newest timestamp, not the oldest.
- Timestamp ties require a reliable source-defined ordering field.
- The highest amount does not necessarily represent the latest record.
- Use `WHERE status = 'Completed'`, not `status <> 'Cancelled'`, when the requirement is Completed sales only.
- Use standard SQL equality (`=`) and single quotes for string literals.
- Ensure CTEs expose the columns required by downstream joins.

### Python — Completed

- Improved `normalize_sale()` with separate exception handling for `sale_id` and `amount`.
- Introduced field-specific rejection codes: `INVALID_SALE_ID` and `INVALID_AMOUNT`.
- Used `raise ValueError(...) from exc` to preserve the original exception.
- Updated `normalize_records()` to capture the error message using `str(exc)`.
- Preserved original raw records using `record.copy()`.
- Verified that malformed records are rejected without preventing subsequent valid records from processing.
- Added an automated test for invalid sale IDs.
- Updated the existing normalization recovery test to expect `INVALID_AMOUNT`.

### Python — Key Learning

- Exception handling should distinguish conversion errors by field.
- Normalizing one record and managing a batch of records are separate responsibilities.
- `normalize_sale()` converts data or raises an error.
- `normalize_records()` catches record-level failures and maintains the rejection collection.
- Raising an exception stops the current function's normal execution.
- One rejected record should not accidentally generate multiple rejection entries.
- Preserve original source values for auditing and reprocessing.

### Test Status

- Last confirmed complete suite: 14 tests passed.
- Added one new invalid-sale-ID test.
- Expected total: 15 tests, pending confirmation by running pytest.

### Remaining Python Gaps

- Handle missing CSV columns without unexpected `KeyError` failures.
- Improve schema validation and malformed-row handling.
- Use `Decimal` for financial amounts rather than `float`.
- Handle non-finite numeric values and other edge cases.
- Integrate `run_batch()` consistently into the pipeline entry point.
- Add complete batch reconciliation and end-to-end testing.
- Improve structured logging and audit information.

### Remaining SQL Gaps

- Save completed advanced SQL exercises in the repository.
- Practise harder CTE, subquery, and date/time scenarios.
- Implement incremental loading with watermarks and upserts.
- Practise transactions, audit queries, and reconciliation.
- Learn query execution plans, indexing, and SQL performance troubleshooting.

### Next Starting Point

**Python:** Verify all tests, then implement missing-field and schema-validation handling.

**SQL:** Continue advanced business scenarios involving incremental loads, date logic, and complex joins.

**Overall objective:** Develop independent, production-oriented Python and SQL proficiency for data-engineering roles and technical interviews.

## October 21, 2026 — Python Missing-Field Handling and SQL Incremental Date Filtering

### Python — Completed

- Reviewed the difference between dictionary indexing (`record["key"]`) and safe retrieval (`record.get("key")`).
- Identified why accessing a missing dictionary key raises `KeyError`.
- Updated `normalize_sale()` to handle missing `sale_id` and `amount` fields safely.
- Standardized missing and empty numeric fields to `None`.
- Preserved `INVALID_SALE_ID` and `INVALID_AMOUNT` exceptions for malformed numeric strings.
- Added two normalization tests for missing numeric fields.
- Reviewed the difference between normalization and business validation.

### Python — Key Learning

- `record["key"]` raises `KeyError` when the key is missing.
- `record.get("key")` returns `None` when the key is missing.
- Converting a local variable does not automatically update its source dictionary.
- Normalization converts data into standardized types.
- Business validation determines whether a normalized record satisfies business rules.
- A missing `sale_id` can be normalized to `None` before being rejected by `process_sales()`.
- A missing amount is rejected by business validation when `status = "Completed"`.
- Cancelled records with missing amounts may still be accepted under the current business rules.

### SQL — Completed

- Practised timestamp filtering for daily incremental data extraction.
- Identified sale IDs within a specified daily loading window.
- Compared `BETWEEN` with inclusive-start and exclusive-end filtering.
- Corrected an end-of-day boundary that could omit fractional-second timestamps.
- Implemented an incremental date-range SQL query using `>=` and `<`.
- Practised ascending timestamp ordering.

### SQL — Key Learning

- Incremental loading can process only records that fall within a defined time window.
- Half-open intervals include the starting boundary and exclude the ending boundary.
- `BETWEEN` includes both boundaries and can cause issues with timestamp precision.
- Prefer `updated_at >= start_watermark AND updated_at < end_watermark`.
- Production watermarks should be parameterized rather than hardcoded.
- Timestamp-based incremental filtering alone does not guarantee exactly-once processing.

### Testing Checkpoint

- Two missing-field normalization tests added.
- Full pytest suite must be rerun to confirm the updated passing-test count.

### Next Session

**Python:** Improve validation for malformed CSV structures, unexpected data types, and complete pipeline integration.

**SQL:** Implement persisted incremental-load watermarks, late-arriving records, and idempotent loading.

**Long-term objective:** Independently build, test, troubleshoot, and explain reliable Python and SQL data-engineering pipelines.

## October 26, 2026 — Python and SQL Session

### Python
- Implemented CSV required-header validation.
- Detected extra and missing CSV cells.
- Distinguished empty cells from missing cells.
- Added pytest tests for malformed CSV structures.
- Implemented source-to-output count reconciliation.
- Reviewed normalization vs business validation.

### SQL
- Practised LEFT JOIN anti-join and NOT EXISTS.
- Reviewed correlated subquery execution.
- Identified new and updated source records.
- Used ROW_NUMBER and CTEs for deduplication.
- Studied MERGE and idempotency.
- Reviewed transactions, COMMIT and ROLLBACK.
- Understood timestamp watermarks and late arrivals.
- Learned authoritative source-version ordering.

### Verification
- Previous test run: 20 passed, 1 failed.
- Missing-cell test corrected; final run pending.

### Next Session
- Python: Automated reconciliation and integration tests.
- SQL: Ingestion timestamps, late-arriving data,
  persisted watermarks and executable MERGE scenarios.