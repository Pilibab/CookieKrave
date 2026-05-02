from typing import Dict, Any 
from app.repository.customer_repo import CustomerRepository
# from app.repository.inventory_repo import InventoryRepository
# from app.repository.cart_repo import CartRepository # Don't forget to import this!

from app.model.customer import CustomerCreate
class SupplyChainService:
    def __init__(
        self, 
        cust_repo: CustomerRepository, 
    ):
        self.cust_repo = cust_repo

    def cust_sign_in(self, cust_info: Dict[str, Any]):
        cust_to_Create = CustomerCreate(**cust_info)
        
        self.cust_repo.create(cust_to_Create)


