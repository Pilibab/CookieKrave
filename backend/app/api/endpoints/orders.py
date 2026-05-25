# backend/app/api/endpoints/orders.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client
from uuid import UUID


from app.model.order import Order, OrderCreate
from app.repository.orders_repo import OrderRepository
from app.db.supabase_client import supabase

def get_supabase():
    """Returns the globally initialized supabase client."""
    return supabase

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
    response_model=Order, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order"
)
def create_order(
    order_in: OrderCreate, 
    repo: OrderRepository = Depends(get_order_repository)
):
    """
    Creates a new order record.
    """
    return repo.create(order_in)


@router.get(
    "", 
    response_model=List[Order], 
    summary="Retrieve all orders"
)
def get_all_orders(
    repo: OrderRepository = Depends(get_order_repository)
):
    """
    Retrieves all orders from the database.
    """
    return repo.get_all()


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
    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No orders found for customer {customer_id}."
        )
    return orders


@router.put(
    "/{order_id}", 
    response_model=Order, 
    summary="Update an existing order"
)
def update_order(
    order_id: int, 
    order_data: Order, 
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
        
    updated_records = repo.update(str(order_id), order_data)
    
    if not updated_records:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update order record."
        )
        
    return updated_records[0]


@router.delete(
    "/{order_id}", 
    summary="Delete an order"
)
def delete_order(
    order_id: int, 
    repo: OrderRepository = Depends(get_order_repository)
):
    """
    Deletes an order record permanently from the database.
    """
    if not repo.get_by_id(order_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Order with ID {order_id} not found."
        )
        
    repo.delete(str(order_id))
    return {"message": f"Order {order_id} has been permanently deleted."}
