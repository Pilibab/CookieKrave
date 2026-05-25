from typing import Any, List, Dict
from app.repository.orders_repo import OrderRepository
from app.repository.product_repo import ProductRepository
from app.repository.cart_repo import CartRepository # Don't forget to import this!

from app.model.order import OrderCreate

class OrderService:
    def __init__(
        self, 
        order_repo: OrderRepository, 
        prod_repo: ProductRepository, 
        cart_repo: CartRepository
    ):
        self.order_repo = order_repo
        self.prod_repo = prod_repo
        self.cart_repo = cart_repo # Fixed: Now properly assigned

    # ? wont it be better to fetch also or ensure that the returned query 
    # ? contains cust_id that way we ensure that the grabbed query is made by the customer
    def get_final_bill(self, order_id: int, cust_id: int) -> Dict[str, Any]:
        # 1. Fetch data
        order = self.order_repo.get_by_id(order_id)
        
        # Guard clause: Check if order exists before accessing attributes
        if not order:
            raise ValueError(f"Order with ID {order_id} not found.")

        items = self.cart_repo.get_items_by_order(order_id)
        
        bill_details: List[Dict[str, Any]] = []
        grand_total: float = 0.0

        # 2. Stitch the data together
        for item in items:
            product = self.prod_repo.get_by_id(item.prod_id)
            
            # Guard clause: Check if product exists in inventory
            if product is None:
                continue # Skip this item if product doesn't exist
            
            line_total = float(item.cart_quan * product.prod_price)
            grand_total += line_total
            
            bill_details.append({
                "product": product.prod_name,
                "quantity": item.cart_quan,
                "prod_price": product.prod_price,
                "subtotal": line_total
            })

        return {
            "order_no": order.ord_id,
            "date": order.ord_time,
            "total": grand_total,
            "items": bill_details
        }

    def create_order(self, order_details: Dict[str, Any]) -> Dict[str, Any]:
        """
            creates order instance and populate cart table 
            args: { 
                cust_id,
                total_amount,
                ord_pay_meth, 
                ord_f_type, 
                prod_ids: list[int | str]}
        """
        order_to_create = OrderCreate(
            cust_id= order_details["cust_id"],
            total_amount=order_details["total_amount"],
            ord_pay_meth= order_details["ord_pay_meth"],
            ord_f_type= order_details["ord_f_type"]
        )

        ordered_prod =  order_details["prod_ids"]

        try:
            # create order instance
            new_order = self.order_repo.create(order_to_create)

            # populate cart 
            self.cart_repo.create_order_line(order_id=new_order.ord_id, items=ordered_prod)

            return {
                "status": "Success",
                "order_id": new_order.ord_id,
                "time": new_order.ord_time
            }
        
        except Exception as e:
            return {
                "status": "Failed",
                "error": str(e)
            }



