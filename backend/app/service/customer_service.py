from typing import Any
from uuid import UUID
from app.repository.customer_repo import CustomerRepository
from app.model.customer import CustomerCreate

class SupplyChainService:
    def __init__(
        self, 
        cust_repo: CustomerRepository, 
    ):
        self.cust_repo = cust_repo

    # Inside your SupplyChainService or CustomerRepository:
    def create_social_customer_if_absent(
        self, 
        cust_info: dict[str, Any],
        social_id: UUID
        ):

        if not self.cust_repo.is_user_registered(social_id):
            # If they don't exist, create them using your standard repository logic
            customer_to_create = CustomerCreate(**cust_info)
            return self.cust_repo.create(customer_to_create)
            
        return self.cust_repo.get_by_id(social_id)


