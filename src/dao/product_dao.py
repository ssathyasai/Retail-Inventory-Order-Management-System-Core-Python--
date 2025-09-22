from typing import Optional, List, Dict
from src.config import get_supabase

def _sb():
    return get_supabase()

def create_product(name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Optional[Dict]:
    payload = {"name": name, "sku": sku, "price": price, "stock": stock}
    if category:
        payload["category"] = category
    _sb().table("products").insert(payload).execute()
    resp = _sb().table("products").select("*").eq("sku", sku).limit(1).execute()
    return resp.data[0] if resp.data else None

def get_product_by_id(prod_id: int) -> Optional[Dict]:
    resp = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
    return resp.data[0] if resp.data else None

def get_product_by_sku(sku: str) -> Optional[Dict]:
    resp = _sb().table("products").select("*").eq("sku", sku).limit(1).execute()
    return resp.data[0] if resp.data else None

def update_product(prod_id: int, fields: Dict) -> Optional[Dict]:
    _sb().table("products").update(fields).eq("prod_id", prod_id).execute()
    resp = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
    return resp.data[0] if resp.data else None

def list_products(limit: int = 100, category: str | None = None) -> List[Dict]:
    q = _sb().table("products").select("*").order("prod_id", desc=False).limit(limit)
    if category:
        q = q.eq("category", category)
    resp = q.execute()
    return resp.data or []
