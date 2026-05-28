# backend/app/api/endpoints/cart.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client


from app.model.cart import Cart, CartCreate
from app.repository.cart_repo import CartRepository
from app.db.supabase_client import supabase

def get_supabase():
    """Returns the globally initialized supabase client."""
    return supabase

def get_cart_repository(supabase: Client = Depends(get_supabase)) -> CartRepository:
    """Provides an instance of the CartRepository with the database connection injected."""
    return CartRepository(supabase)

# Define the router
router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

@router.post(
    "", 
    response_model=Cart, 
    status_code=status.HTTP_201_CREATED,
    summary="Add item to cart"
)
def create_cart_item(
    cart_in: CartCreate, 
    repo: CartRepository = Depends(get_cart_repository)
):
    """
    Adds a new item to the cart.
    """
    return repo.create(cart_in)


@router.get(
    "", 
    response_model=List[Cart], 
    summary="Retrieve all cart items"
)
def get_all_cart_items(
    repo: CartRepository = Depends(get_cart_repository)
):
    """
    Retrieves all cart items from the database.
    """
    return repo.get_all()


@router.get(
    "/order/{order_id}", 
    response_model=List[Cart], 
    summary="Get cart items by order ID"
)
def get_cart_items_by_order(
    order_id: int, 
    repo: CartRepository = Depends(get_cart_repository)
):
    """
    Retrieves all cart items for a specific order.
    """
    items = repo.get_items_by_order(order_id)
    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No cart items found for order {order_id}."
        )
    return items


@router.delete(
    "/order/{order_id}/product/{product_id}", 
    summary="Remove item from cart"
)
def delete_cart_item(
    order_id: int,
    product_id: int,
    repo: CartRepository = Depends(get_cart_repository)
):
    """
    Removes a specific product from a cart/order.
    """
    # Verify the item exists by checking the order's cart
    item_exists = repo.check_item_in_cart(order_id, product_id)
    
    if not item_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Product {product_id} not found in order {order_id}."
        )
    
    # Cart items are identified by ORD_ID and PROD_ID, so we delete based on those
    repo.table.delete().eq("ORD_ID", order_id).eq("PROD_ID", product_id).execute()
    return {"message": f"Product {product_id} removed from order {order_id}."}


@router.post(
    "/order/{order_id}/bulk", 
    response_model=List[Cart], 
    status_code=status.HTTP_201_CREATED,
    summary="Add multiple items to cart"
)
def create_order_line_items(
    order_id: int,
    items: List[dict[str, int]], 
    repo: CartRepository = Depends(get_cart_repository)
):
    """
    Creates multiple cart items for an order at once.
    Expected format: [{"PROD_ID": 101, "CART_QUAN": 2}, ...]
    """
    repo.create_order_line(order_id, items)

    # Return the created items
    return repo.get_items_by_order(order_id)
