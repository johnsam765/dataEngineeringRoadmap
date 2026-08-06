from src.transformations.sales_baseline import process_sales

def test_valid_completed_sales_are_accepted_and_summarized():
    records = [
        {
            "sale_id": 1,
            "region": "East",
            "amount": 100.0,
            "status": "Completed",
        },
        {
            "sale_id": 2,
            "region": "East",
            "amount": 50.0,
            "status": "Completed",
        },
    ]

    result = process_sales(records)
    assert len(result["accepted_records"]) == 2
    assert len(result["rejected_records"]) == 0
    assert result['regional_summary']["East"]['completed_order_count'] == 2
    assert result['regional_summary']["East"]['completed_sales_amount'] == 150.0

def test_cancelled_sale_is_accepted_but_not_summarized():
    records = [
        {
            "sale_id": 1,
            "region": "East",
            "amount": 50.0,
            "status": "Cancelled",
        }
    ]

    result = process_sales(records)
    assert len(result["accepted_records"]) == 1
    assert len(result["rejected_records"]) == 0
    assert result["regional_summary"] == {}

def test_duplicate_sale_id_is_rejected():
    records = [
        {
            "sale_id": 1,
            "region": "East",
            "amount": 100.0,
            "status": "Completed",
        },
        {
            "sale_id": 1,
            "region": "East",
            "amount": 200.0,
            "status": "Completed",
        },
    ]

    result = process_sales(records)

    assert len(result["accepted_records"]) == 1
    assert len(result["rejected_records"]) == 1
    assert result["accepted_records"][0] == records[0]
    assert result["rejected_records"][0]["record"] == records[1]
    assert result["rejected_records"][0]["reason"] == "duplicate_sale_id"
    assert result["regional_summary"]["East"]['completed_order_count'] == 1
    assert result["regional_summary"]["East"]['completed_sales_amount'] == 100.0

def test_missing_sale_id_key_is_rejected_without_error():
    records = [
        {
            "region": "North",
            "amount": 300.0,
            "status": "Completed",
        }
    ]
    
    result=process_sales(records)
    assert len(result["accepted_records"]) == 0
    assert len(result["rejected_records"]) == 1
    assert result["rejected_records"][0]["record"] == records[0]
    assert result["rejected_records"][0]["reason"] == "missing_sale_id"
    assert result["regional_summary"] == {}

def test_process_sales_uses_supplied_records_only():
    records = [
        {
            "sale_id": 9999,
            "region": "Central",
            "amount": 325.0,
            "status": "Completed",
        }
    ]

    result = process_sales(records)

    assert result == {
        "accepted_records": records,
        "rejected_records": [],
        "regional_summary": {
            "Central": {
                "completed_order_count": 1,
                "completed_sales_amount": 325.0,
            }
        },
    }