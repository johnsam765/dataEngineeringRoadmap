sales = [
    {
        "sale_id": 1001,
        "region": "East",
        "amount": 120.00,
        "status": "Completed",
    },
    {
        "sale_id": 1002,
        "region": "East",
        "amount": 80.00,
        "status": "Completed",
    },
    {
        "sale_id": 1003,
        "region": "East",
        "amount": 50.00,
        "status": "Cancelled",
    },
    {
        "sale_id": 1004,
        "region": "West",
        "amount": 200.00,
        "status": "Completed",
    },
    {
        "sale_id": 1004,
        "region": "West",
        "amount": 200.00,
        "status": "Completed",
    },
    {
        "sale_id": 1005,
        "region": None,
        "amount": 150.00,
        "status": "Completed",
    },
    {
        "sale_id": 1006,
        "region": "West",
        "amount": None,
        "status": "Completed",
    },
    {
        "sale_id": None,
        "region": "North",
        "amount": 300.00,
        "status": "Completed",
    },
]

def validate_sale(sale, seen_sale_ids) -> tuple[bool,str|None]:
    if sale.get("sale_id") in (None,""):
        return (False, "missing_sale_id")
    if sale.get("region") is None or sale.get("region")=="":
        return (False, "missing_region")
    if sale.get("status") == "Completed" and sale.get("amount") is None:
        return (False, "missing_completed_amount")
    if sale.get("sale_id") in seen_sale_ids:
        return (False, "duplicate_sale_id")
    return (True, None)


def summarize_completed_sale(
    regional_summary: dict,
    sale: dict,
) -> None:
    if sale.get("status") != "Completed":
        return
    region=sale.get("region")
    amount=sale.get("amount")
    if region not in regional_summary:
        regional_summary[region]={
             "completed_order_count": 0,
             "completed_sales_amount": 0,
        }
    regional_summary[region]["completed_order_count"]+=1
    regional_summary[region]["completed_sales_amount"]+=amount

def process_sales(records: list[dict]) -> dict:
    accepted_records = []
    rejected_records = []
    regional_summary = {}
    seen_sale_ids = set()
    for sale in records:
        is_valid,rejection_result=validate_sale(sale,seen_sale_ids)
        if not is_valid:
            rejected_records.append({"record":sale,"reason":rejection_result})
            continue
        seen_sale_ids.add(sale.get("sale_id"))
        accepted_records.append(sale)
        summarize_completed_sale(regional_summary, sale)
    return {
        "accepted_records":accepted_records,
        "rejected_records":rejected_records,
        "regional_summary":regional_summary
     }
     
if __name__ == "__main__":
    print(process_sales(sales))