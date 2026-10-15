from pathlib import Path
from src.transformations.sales_baseline import process_sales
from src.output.json_writer import write_json
import csv

ROOT=Path(__file__).resolve().parent.parent.parent
SALES_ROOT=ROOT/"data"/"raw"/"sales.csv"

def read_sales_csv(file_path:Path) -> list[dict]:
    with file_path.open("r",encoding="utf-8",newline="") as file_content:
        return list(csv.DictReader(file_content))

def normalize_sale(record:dict) -> dict:
    record["sale_id"]=None if record["sale_id"]=="" else int(record["sale_id"])
    record["amount"]=None if record["amount"]=="" else float(record["amount"])
    return record

if __name__=="__main__":
    records=read_sales_csv(SALES_ROOT)
    normalized_records=[normalize_sale(record) for record in records]
    result = process_sales(normalized_records)
    write_json(result["accepted_records"],ROOT/"data"/"processed"/"accepted_sales.json")
    write_json(result["rejected_records"],ROOT/"data"/"rejected"/"rejected_sales.json")
    print(result)

