"""Create deterministic synthetic source data for RevenueRadar."""
from pathlib import Path
import csv, random

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
random.seed(42)
products = [
    ("P-100", "Atlas Pro", "Software", 1200, 0.15, 410),
    ("P-200", "Nimbus Core", "Software", 800, 0.10, 270),
    ("P-300", "Orbit Desk", "Hardware", 450, 0.08, 255),
    ("P-400", "Vista Kit", "Hardware", 250, 0.05, 155),
]
customers = [("C-01","Northstar Retail","Enterprise","North"),("C-02","Aperture Labs","Mid-market","West"),("C-03","Keystone Group","Enterprise","East"),("C-04","Bluebird Co","SMB","South")]

def write(name, rows, fields):
    with (RAW / name).open("w", newline="") as f: csv.DictWriter(f, fieldnames=fields).writeheader(); csv.DictWriter(f, fieldnames=fields).writerows(rows)

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    write("customers.csv", [dict(customer_id=a,customer_name=b,segment=c,region=d) for a,b,c,d in customers], ["customer_id","customer_name","segment","region"])
    write("price_list.csv", [dict(product_id=a,product_name=b,category=c,list_price=d,approved_discount_pct=e,cogs_unit_price=f) for a,b,c,d,e,f in products], ["product_id","product_name","category","list_price","approved_discount_pct","cogs_unit_price"])
    orders, returns = [], []
    for i in range(1, 121):
        pid, _, _, price, approved, cogs = random.choice(products); cid, _, _, _ = random.choice(customers)
        qty = random.randint(1, 8); extra = 0.12 if i % 13 == 0 else (0.06 if i % 7 == 0 else 0)
        discount = round(min(approved + extra, .35), 2); unit_price = round(price * (1 - discount) * (0.94 if i % 17 == 0 else 1), 2)
        order = {"order_id":f"ORD-{i:04}","order_date":f"2026-{(i-1)//30+1:02}-{(i-1)%28+1:02}","customer_id":cid,"product_id":pid,"quantity":qty,"invoiced_unit_price":unit_price,"discount_pct":discount,"cogs_unit_price":cogs}
        orders.append(order)
        if i % 11 == 0: returns.append({"return_id":f"RET-{i:04}","order_id":order["order_id"],"return_value":round(unit_price*qty*(.25 if i%22 else .7),2),"return_reason":"Damaged" if i%22 else "Buyer remorse"})
    write("orders.csv", orders, list(orders[0])); write("returns.csv", returns, ["return_id","order_id","return_value","return_reason"])
if __name__ == "__main__": main()

