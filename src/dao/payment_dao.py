from typing import Optional, Dict
from src.config import get_supabase

_sb = get_supabase()

def create_payment(order_id: int, amount: float) -> Dict:
    payload = {"order_id": order_id, "amount": amount, "method": None, "status": "PENDING"}
    _sb.table("payments").insert(payload).execute()
    resp = _sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
    return resp.data[0] if resp.data else {}

def process_payment(order_id: int, method: str) -> Dict:
    _sb.table("payments").update({"method": method, "status": "PAID"}).eq("order_id", order_id).execute()
    _sb.table("orders").update({"status": "COMPLETED"}).eq("order_id", order_id).execute()
    resp = _sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
    return resp.data[0] if resp.data else {}

def refund_payment(order_id: int) -> Dict:
    _sb.table("payments").update({"status": "REFUNDED"}).eq("order_id", order_id).execute()
    resp = _sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
    return resp.data[0] if resp.data else {}
