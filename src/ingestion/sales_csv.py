from pathlib import Path
from src.transformations.sales_baseline import process_sales
from src.output.json_writer import write_json
import csv

ROOT=Path(__file__).resolve().parent.parent.parent
SALES_ROOT=ROOT/"data"/"raw"/"sales.csv"

def read_sales_csv(file_path:Path) -> list[dict]:
    required_columns={"sale_id","region","amount","status"}
    with file_path.open("r",encoding="utf-8",newline="") as file_content:
        reader=csv.DictReader(file_content)
        actual_columns=set(reader.fieldnames or [])
        missing_columns=required_columns-actual_columns
        if missing_columns:
            raise ValueError(f"MISSING_REQUIRED_COLUMNS: {', '.join(sorted(missing_columns))}")
        records=[]
        for i in reader:
            if None in i:
                raise ValueError("EXTRA_CSV_VALUES")
            if any(j is None for j in i.values()):
                raise ValueError("MISSING_CSV_VALUES")
            records.append(i)
        return records

def normalize_sale(record: dict) -> dict:
    raw_sale_id = record.get("sale_id")
    raw_sale_amount = record.get("amount")
    try:
        record["sale_id"] = (
            None if raw_sale_id in (None, "")
            else int(raw_sale_id)
        )
    except ValueError as exc:
        raise ValueError("INVALID_SALE_ID") from exc

    try:
        record["amount"] = (
            None if raw_sale_amount in (None, "")
            else float(raw_sale_amount)
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
    source_count = len(records)
    accepted_count = len(result["accepted_records"])
    rejected_count = len(result["rejected_records"])
    if source_count != accepted_count + rejected_count:
        raise RuntimeError(
            f"RECONCILIATION_FAILED: source={source_count}, "
            f"accepted={accepted_count}, rejected={rejected_count}"
        )
    print(
        f"RECONCILIATION_PASSED: source={source_count}, "
        f"accepted={accepted_count}, rejected={rejected_count}"
    )
    write_json(result["accepted_records"],ROOT/"data"/"processed"/"accepted_sales.json")
    write_json(result["rejected_records"],ROOT/"data"/"rejected"/"rejected_sales.json")
    print(result)

