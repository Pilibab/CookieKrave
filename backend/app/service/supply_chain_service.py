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
            #get all inv_id that has matching prod_id
            recipe = self.bom_repo.get_stock(item.prod_id)

            for ingredient in recipe:
                # Get the raw material info from Inventory
                total_needed : float = ingredient.bom_quan_req * item.cart_quan
                material_id : int = ingredient.inv_id

                # Logic to subtract stock 
                # sends the negative value of the amount req for decrement hehehe
                self.inventory_repo.adjust_stock(material_id, - total_needed)

    def update_availability(self, prod_id: int) -> bool:
        """
        Checks the bill of materials for a product against current inventory stock.
        Returns True if any required ingredient's quantity meets or exceeds available stock.
        """
        bom_list = self.bom_repo.get_stock(prod_id)

        for ingredient in bom_list:
            # 1. Get the current inventory item details using the ingredient's inv_id
            # (Adjust 'get' to 'get_by_id' or whatever your inventory repo uses to fetch by primary key)
            inventory_item = self.inventory_repo.get_by_id(ingredient.inv_id)
            
            if inventory_item:
                # 2. Check if the required quantity is greater than or equal to the current stock
                if ingredient.bom_quan_req >= inventory_item.inv_stock:
                    # 3. Stop processing immediately and return True
                    return True
                    
        # If all ingredients have enough stock, return False
        return False


        

