from src.config import get_supabase
from datetime import datetime, timedelta

_sb = get_supabase()

def top_selling_products(limit: int = 5):
    resp = _sb.table("order_items").select("prod_id, quantity").execute()
    counts = {}
    for item in resp.data or []:
        counts[item["prod_id"]] = counts.get(item["prod_id"], 0) + item["quantity"]
    top5 = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    return top5

def total_revenue_last_month():
    today = datetime.utcnow()
    start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    end = start.replace(day=28) + timedelta(days=4)
    end = end.replace(day=1)
    resp = _sb.table("payments").select("amount").eq("status", "PAID").gte("paid_at", start.isoformat()).lt("paid_at", end.isoformat()).execute()
    total = sum(item["amount"] for item in resp.data or [])
    return total

def orders_per_customer():
    resp = _sb.table("orders").select("cust_id").execute()
    counts = {}
    for o in resp.data or []:
        counts[o["cust_id"]] = counts.get(o["cust_id"], 0) + 1
    return counts

def frequent_customers(min_orders: int = 2):
    counts = orders_per_customer()
    return [cust_id for cust_id, cnt in counts.items() if cnt > min_orders]
