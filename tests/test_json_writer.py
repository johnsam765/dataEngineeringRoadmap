import json
from src.output.json_writer import write_json


def test_write_json(tmp_path):
    # ARRANGE
    records = [
        {"sale_id": 1001, "amount": 120.0}
    ]

    output_path = tmp_path / "processed" / "accepted_sales.json"

    # ACT
    write_json(records, output_path)

    # ASSERT
    assert output_path.exists()

    saved_records = json.loads(
        output_path.read_text(encoding="utf-8")
    )

    assert saved_records == records