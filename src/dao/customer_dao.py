from typing import Optional, List, Dict
from src.config import get_supabase

_sb = get_supabase()

def create_customer(name: str, email: str, phone: str, city: str | None = None) -> Dict:
    existing = _sb.table("customers").select("*").eq("email", email).limit(1).execute()
    if existing.data:
        raise ValueError(f"Customer with email '{email}' already exists")
    payload = {"name": name, "email": email, "phone": phone}
    if city:
        payload["city"] = city
    _sb.table("customers").insert(payload).execute()
    resp = _sb.table("customers").select("*").eq("email", email).limit(1).execute()
    return resp.data[0] if resp.data else {}

def update_customer(cust_id: int, phone: str | None = None, city: str | None = None) -> Dict:
    fields = {}
    if phone:
        fields["phone"] = phone
    if city:
        fields["city"] = city
    if not fields:
        raise ValueError("Nothing to update")
    _sb.table("customers").update(fields).eq("cust_id", cust_id).execute()
    resp = _sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
    return resp.data[0] if resp.data else {}

def delete_customer(cust_id: int) -> Dict:
    orders = _sb.table("orders").select("*").eq("cust_id", cust_id).limit(1).execute()
    if orders.data:
        raise ValueError("Cannot delete customer with existing orders")
    resp_before = _sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
    row = resp_before.data[0] if resp_before.data else {}
    _sb.table("customers").delete().eq("cust_id", cust_id).execute()
    return row

def list_customers(limit: int = 100) -> List[Dict]:
    resp = _sb.table("customers").select("*").order("cust_id", desc=False).limit(limit).execute()
    return resp.data or []

def search_customers(email: str | None = None, city: str | None = None) -> List[Dict]:
    q = _sb.table("customers").select("*")
    if email:
        q = q.eq("email", email)
    if city:
        q = q.eq("city", city)
    resp = q.execute()
    return resp.data or []

def get_customer(cust_id: int) -> Optional[Dict]:
    resp = _sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
    return resp.data[0] if resp.data else None
