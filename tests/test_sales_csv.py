from src.ingestion.sales_csv import read_sales_csv,normalize_sale
import pytest

def test_read_sales_csv(tmp_path):
    csv_file = tmp_path / "sales.csv"
    csv_file.write_text(
    """sale_id,region,amount,status
1001,East,120.00,Completed
1002,West,80.00,Completed
""",
    encoding="utf-8"
)
    records=read_sales_csv(csv_file)
    assert len(records) == 2
    assert records[0]["sale_id"] == "1001"
    assert records[1]["sale_id"] == "1002"

def test_normalize_functionality(tmp_path):
    csv_file = tmp_path / "sales.csv"
    csv_file.write_text(
    """sale_id,region,amount,status
1001,East,120.00,Completed
""",
    encoding="utf-8"
)
    records=read_sales_csv(csv_file)
    normalized_record=normalize_sale(records[0])

    assert isinstance(normalized_record["sale_id"], int)
    assert isinstance(normalized_record["amount"], float)
    assert normalized_record["sale_id"] == 1001
    assert normalized_record["amount"] == 120.0

def test_normalize_functionality_none_case(tmp_path):
    csv_file = tmp_path / "sales.csv"
    csv_file.write_text(
    """sale_id,region,amount,status
,East,,Completed
""",
    encoding="utf-8"
)
    records=read_sales_csv(csv_file)
    normalized_record=normalize_sale(records[0])
    assert normalized_record["sale_id"] is None
    assert normalized_record["amount"] is None

def test_normalize_invalid_amount():
    record = {
        "sale_id": "1001",
        "region": "East",
        "amount": "abc",
        "status": "Completed"
    }
    with pytest.raises(ValueError):
        normalize_sale(record)


