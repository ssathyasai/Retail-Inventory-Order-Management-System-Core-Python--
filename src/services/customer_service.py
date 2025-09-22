from typing import Dict, List
from src.dao.customer_dao import CustomerDAO

class CustomerError(Exception):
    pass

class CustomerService:
    def __init__(self):
        self.dao = CustomerDAO()

    def create_customer(self, name: str, email: str, phone: str, city: str | None = None) -> Dict:
        try:
            return self.dao.create_customer(name, email, phone, city)
        except ValueError as e:
            raise CustomerError(str(e))

    def update_customer(self, cust_id: int, phone: str | None = None, city: str | None = None) -> Dict:
        fields = {}
        if phone:
            fields["phone"] = phone
        if city:
            fields["city"] = city
        if not fields:
            raise CustomerError("Nothing to update")
        return self.dao.update_customer(cust_id, fields)

    def delete_customer(self, cust_id: int) -> Dict:
        try:
            return self.dao.delete_customer(cust_id)
        except ValueError as e:
            raise CustomerError(str(e))

    def list_customers(self) -> List[Dict]:
        return self.dao.list_customers()

    def search_customers(self, email: str | None = None, city: str | None = None) -> List[Dict]:
        return self.dao.search_customers(email, city)
