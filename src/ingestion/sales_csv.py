from pathlib import Path
from src.transformations.sales_baseline import process_sales
from src.output.json_writer import write_json
import csv

ROOT=Path(__file__).resolve().parent.parent.parent
SALES_ROOT=ROOT/"data"/"raw"/"sales.csv"

def read_sales_csv(file_path:Path) -> list[dict]:
    with file_path.open("r",encoding="utf-8",newline="") as file_content:
        return list(csv.DictReader(file_content))

def normalize_sale(record: dict) -> dict:
    try:
        record["sale_id"] = (
            None if record["sale_id"] == ""
            else int(record["sale_id"])
        )
    except ValueError as exc:
        raise ValueError("INVALID_SALE_ID") from exc

    try:
        record["amount"] = (
            None if record["amount"] == ""
            else float(record["amount"])
        )
    except ValueError as exc:
        raise ValueError("INVALID_AMOUNT") from exc

    return record

def normalize_records(records: list[dict]) -> tuple[list[dict], list[dict]]:
    normalized_records=[]
    normalization_rejections=[]
    for record in records:
        try:
            normalized_record=normalize_sale(record.copy())
            normalized_records.append(normalized_record)
        except ValueError as exc:
            normalization_rejections.append({
                "record": record,
                "reason": str(exc)
            })
    return normalized_records, normalization_rejections


if __name__=="__main__":
    records=read_sales_csv(SALES_ROOT)
    normalized_records, normalization_rejections = normalize_records(records)
    result = process_sales(normalized_records)
    result["rejected_records"].extend(normalization_rejections)
    write_json(result["accepted_records"],ROOT/"data"/"processed"/"accepted_sales.json")
    write_json(result["rejected_records"],ROOT/"data"/"rejected"/"rejected_sales.json")
    print(result)

