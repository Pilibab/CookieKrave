from fastapi import FastAPI, Depends
from app.repository.orders_repo import OrderRepository
from app.repository.product_repo import ProductRepository
from app.repository.cart_repo import CartRepository

from app.service.order_service import OrderService
from app.db.supabase_client import supabase # Your client initialization

app = FastAPI(title="CookieKrave API")

# Dependency Injection (Simple version)
def get_order_service():
    # You initialize your repos and pass them to the service
    order_repo = OrderRepository(supabase)
    cart_repo = CartRepository(supabase)
    prod_repo = ProductRepository(supabase)

    return OrderService(order_repo, prod_repo, cart_repo)

@app.get("/health")
def health_check():
    return {"status": "online", "business": "CookieKrave"}

@app.get("/orders/{order_id}/bill")
def get_bill(order_id: int, service: OrderService = Depends(get_order_service)):
    return service.get_final_bill(order_id)