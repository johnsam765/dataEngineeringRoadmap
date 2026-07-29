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

def process_sales(records):
    accepted_records=[]
    rejected_records=[]
    regional_summary={}
    sale_id=set()
    for sale in records:
        if ((sale["sale_id"] is None) or (sale["region"] is None) or (
            sale["status"] == "Completed" and sale["amount"] is None)
            or (sale["sale_id"] in sale_id)
        ):
            rejected_records.append(sale)
            continue
        sale_id.add(sale["sale_id"])
        accepted_records.append(sale)
        if sale["status"] != "Completed":
            continue
        region=sale["region"]
        amount=sale["amount"]
        if region not in regional_summary:
            regional_summary[region]={
                "completed_order_count":1,
                "completed_sales_amount":amount
            }
        else:
            regional_summary[region]["completed_order_count"]+=1
            regional_summary[region]["completed_sales_amount"]+=amount
    return {"accepted_records": accepted_records,
    "rejected_records": rejected_records,
    "regional_summary": regional_summary}

print(process_sales(sales))
    