# from typing import List
from app.repository.bom_repo import BOMRepository
from app.repository.inventory_repo import InventoryRepository
from app.repository.cart_repo import CartRepository 

# from app.model.order import OrderCreate

class SupplyChainService:
    def __init__(
        self, 
        bom_repo: BOMRepository, 
        inventory_repo: InventoryRepository, 
        cart_repo: CartRepository
    ):
        self.bom_repo = bom_repo
        self.inventory_repo = inventory_repo
        self.cart_repo = cart_repo 

    def update_inventory(self, order_id: int | str):
        """
            updates the inventory when an order is made
        """
        # retrieve all instance with order id from cart 
        # purpose is to get the product id 
        items = self.cart_repo.get_items_by_order(order_id)

        for item in items:
            #get all INV_ID that has matching PROD_ID
            recipe = self.bom_repo.get_stock(item.PROD_ID)

            for ingredient in recipe:
                # Get the raw material info from Inventory
                total_needed : float = ingredient.BOM_QUAN_REQ * item.CART_QUAN
                material_id : int = ingredient.INV_ID

                # Logic to subtract stock 
                # sends the negative value of the amount req for decrement hehehe
                self.inventory_repo.adjust_stock(material_id, - total_needed)



        

