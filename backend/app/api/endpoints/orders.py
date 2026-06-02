# backend/app/api/endpoints/orders.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from supabase import Client
from uuid import UUID
from pydantic import BaseModel
from decimal import Decimal

from app.model.order import Order, OrderUpdate
from app.repository.orders_repo import OrderRepository
from app.repository.product_repo import ProductRepository
from app.repository.cart_repo import CartRepository
from app.repository.fullfillment_repo import FulfillmentRepository
from app.repository.gcash_repo import GCashRepository
from app.service.order_service import OrderService, FinalBillResponse
from app.db.supabase_client import supabase

class CreateOrderRequest(BaseModel):
    cust_id: UUID
    total_amount: Decimal
    ord_pay_meth: str           # "GCash" | "Cash"
    ord_f_type: str             # "Delivery" | "Pick_Up"
    prod_ids: List[int]
    reference_no: Optional[str] = None   # required only if GCash


def get_supabase():
    """Returns the globally initialized supabase client."""
    return supabase

def get_order_service(supabase: Client = Depends(get_supabase)) -> OrderService:
    return OrderService(
        order_repo=OrderRepository(supabase),
        prod_repo=ProductRepository(supabase),
        cart_repo=CartRepository(supabase),
        fulfillment_repo=FulfillmentRepository(supabase),
        gcash_repo=GCashRepository(supabase),
    )


def get_order_repository(supabase: Client = Depends(get_supabase)) -> OrderRepository:
    """Provides an instance of the OrderRepository with the database connection injected."""
    return OrderRepository(supabase)

# Define the router
router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.post(
    "", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order"
)
def create_order(
    payload: CreateOrderRequest,
    service: OrderService = Depends(get_order_service)
):
    """
    Creates a new order record.
    """
    result = service.create_order(payload.model_dump())

    if result["status"] == "Failed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])

    return result


@router.get("", response_model=List[Order], summary="Retrieve all orders")
def get_all_orders(service: OrderService = Depends(get_order_service)):
    return service.order_repo.get_all()

@router.get(
    "/{order_id}", 
    response_model=Order, 
    summary="Get order by ID"
)
def get_order_by_id(
    order_id: int, 
    repo: OrderRepository = Depends(get_order_repository)
):
    """
    Retrieves a single order using its primary key ID.
    """
    order = repo.get_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Order with ID {order_id} not found."
        )
    return order


@router.get(
    "/customer/{customer_id}", 
    response_model=List[Order], 
    summary="Get orders by customer"
)
def get_orders_by_customer(
    customer_id: UUID, 
    repo: OrderRepository = Depends(get_order_repository)
):
    """
    Retrieves all orders made by a specific customer.
    """
    orders = repo.get_orders_by_customer(customer_id)
    # if not orders:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, 
    #         detail=f"No orders found for customer {customer_id}."
    #     )
        
    orders_list: List[Order] = orders if orders else []
        
    return orders_list


@router.put(
    "/{order_id}", 
    response_model=Order, 
    summary="Update an existing order"
)
def update_order(
    order_id: int, 
    order_data: OrderUpdate, 
    repo: OrderRepository = Depends(get_order_repository)
):
    """
    Updates an entire order profile.
    """
    if not repo.get_by_id(order_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Order with ID {order_id} does not exist."
        )
        
    updated_records = repo.update(order_id, order_data)
    
    if not updated_records:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update order record."
        )
        
    return updated_records[0]

@router.get("/{order_id}/bill", summary="Get final bill for an order", response_model=FinalBillResponse)
def get_final_bill(order_id: int, service: OrderService = Depends(get_order_service)) -> FinalBillResponse:
    try:
        return service.get_final_bill(order_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.delete("/{order_id}", summary="Delete an order")
def delete_order(order_id: int, service: OrderService = Depends(get_order_service)):
    if not service.order_repo.get_by_id(order_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_id} not found.")
    service.order_repo.delete(order_id)
    return {"message": f"Order {order_id} deleted."}