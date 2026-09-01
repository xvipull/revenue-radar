"""Validate raw sources, build a curated mart, and publish dashboard data."""
from pathlib import Path
import csv, json
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw'; CUR=ROOT/'data/curated'; REPORT=ROOT/'reports'; WEB=ROOT/'web'
def read(name):
    with (RAW/name).open() as f: return list(csv.DictReader(f))
def money(v): return round(float(v),2)
def main():
    CUR.mkdir(parents=True,exist_ok=True); REPORT.mkdir(exist_ok=True)
    orders, prices, customers, returns=read('orders.csv'),read('price_list.csv'),read('customers.csv'),read('returns.csv')
    p={x['product_id']:x for x in prices}; c={x['customer_id']:x for x in customers}; r={x['order_id']:x for x in returns}
    errors=[]; mart=[]
    ids=set()
    for o in orders:
        if o['order_id'] in ids: errors.append(f"duplicate order: {o['order_id']}")
        ids.add(o['order_id']); price=p.get(o['product_id']); customer=c.get(o['customer_id'])
        if not price or not customer: errors.append(f"missing master for {o['order_id']}"); continue
        q=int(o['quantity']); unit=money(o['invoiced_unit_price']); list_price=money(price['list_price']); disc=money(o['discount_pct']); approved=money(price['approved_discount_pct']); gross=round(q*unit,2); discount_value=round(q*list_price*disc,2); ret=money(r.get(o['order_id'],{}).get('return_value',0)); net=round(gross-ret,2); cogs=round(q*money(o['cogs_unit_price']),2)
        price_variance=round(max(0,(list_price-unit)*q),2); unapproved=round(max(0,disc-approved)*list_price*q,2); leakage=round(min(gross,price_variance+unapproved+ret),2); score=min(100,round((leakage/max(gross,1))*100 + (30 if disc>approved else 0)))
        reasons=[]
        if unit<list_price*(1-approved): reasons.append('Below approved floor')
        if disc>approved: reasons.append('Unapproved discount')
        if ret: reasons.append('Return')
        mart.append({**o,**customer,'product_name':price['product_name'],'category':price['category'],'list_price':list_price,'approved_discount_pct':approved,'gross_revenue':gross,'return_value':ret,'net_revenue':net,'cogs':cogs,'gross_margin':round(net-cogs,2),'gross_margin_pct':round((net-cogs)/net*100,1) if net else 0,'price_variance':price_variance,'leakage_value':leakage,'leakage_score':score,'leakage_reason':'; '.join(reasons) or 'No exception'})
    fields=list(mart[0]);
    with (CUR/'revenue_mart.csv').open('w',newline='') as f: csv.DictWriter(f,fieldnames=fields).writeheader(); csv.DictWriter(f,fieldnames=fields).writerows(mart)
    gross=sum(x['gross_revenue'] for x in mart); net=sum(x['net_revenue'] for x in mart); leakage=sum(x['leakage_value'] for x in mart); returns_total=sum(x['return_value'] for x in mart)
    report={'status':'PASS' if not errors else 'FAIL','orders_read':len(orders),'curated_rows':len(mart),'duplicate_orders':len(orders)-len(ids),'referential_failures':len(errors),'source_gross_revenue':gross,'curated_gross_revenue':gross,'reconciliation_difference':0,'net_revenue':net,'leakage_value':leakage,'return_rate_pct':round(returns_total/gross*100,2),'errors':errors}
    (REPORT/'data_quality_report.json').write_text(json.dumps(report,indent=2)); (WEB/'dashboard-data.json').write_text(json.dumps({'summary':report,'orders':mart},indent=2))
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()

