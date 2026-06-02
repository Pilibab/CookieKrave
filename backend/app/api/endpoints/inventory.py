# backend/app/api/endpoints/inventory.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client


from app.model.inventory import Inventory, InventoryCreate, InventoryUpdate
from app.repository.inventory_repo import InventoryRepository
from app.repository.bom_repo import BOMRepository
from app.repository.cart_repo import CartRepository
from app.service.supply_chain_service import SupplyChainService
from app.db.supabase_client import supabase

def get_bom_repository(): 
    return BOMRepository(supabase)

def get_cart_repository(): 
    return CartRepository(supabase)

def get_supabase():
    """Returns the globally initialized supabase client."""
    return supabase

def get_inventory_repository(supabase: Client = Depends(get_supabase)) -> InventoryRepository:
    """Provides an instance of the InventoryRepository with the database connection injected."""
    return InventoryRepository(supabase)

def get_supply_chain_service(
    bom_repo: BOMRepository = Depends(get_bom_repository),
    inventory_repo: InventoryRepository = Depends(get_inventory_repository),
    cart_repo: CartRepository = Depends(get_cart_repository)
) -> SupplyChainService:
    return SupplyChainService(bom_repo, inventory_repo, cart_repo)
# Define the router instead of importing app
router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)

@router.post(
    "", 
    response_model=Inventory, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new inventory item"
)
def create_inventory(
    inventory_in: InventoryCreate, 
    repo: InventoryRepository = Depends(get_inventory_repository)
):
    """
    Creates a new inventory item record.
    """
    # Uses inherited BaseRepository.create()
    return repo.create(inventory_in)


@router.get(
    "", 
    response_model=List[Inventory], 
    summary="Retrieve all inventory items"
)
def get_inventories(
    repo: InventoryRepository = Depends(get_inventory_repository)
):
    """
    Retrieves all inventory items from the database.
    """
    # Case: Return all inventory items
    return repo.get_all()


@router.get(
    "/{inv_id}", 
    response_model=Inventory, 
    summary="Get inventory item by ID"
)
def get_inventory_by_id(
    inv_id: int, 
    repo: InventoryRepository = Depends(get_inventory_repository)
):
    """
    Retrieves a single inventory item using its primary key ID.
    """
    inventory = repo.get_by_id(inv_id)
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Inventory item with ID {inv_id} not found."
        )
    return inventory


@router.post(
    "/deduct-by-order/{order_id}",
    summary="Deduct inventory based on an order's cart items"
)
def deduct_inventory_by_order(
    order_id: int,
    service: SupplyChainService = Depends(get_supply_chain_service)
):
    service.update_inventory(order_id)
    return {"message": f"Inventory updated for order {order_id}."}

@router.delete(
    "/{inv_id}", 
    summary="Delete an inventory item"
)
def delete_inventory(
    inv_id: int, 
    repo: InventoryRepository = Depends(get_inventory_repository)
):
    """
    Deletes an inventory item record permanently from the database.
    """
    if not repo.get_by_id(inv_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Inventory item with ID {inv_id} not found."
        )
        
    repo.delete(inv_id)
    return {"message": f"Inventory item {inv_id} has been permanently deleted."}


@router.patch(
    "/{inv_id}/adjust-stock", 
    response_model=Inventory, 
    summary="Adjust inventory stock"
)
def adjust_inventory_stock(
    inv_id: int,
    amount: float,
    repo: InventoryRepository = Depends(get_inventory_repository)
):
    """
    Adjusts the inventory stock by the specified amount.
    - Use a positive amount to restock.
    - Use a negative amount to deduct from stock.
    """
    if not repo.get_by_id(inv_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Inventory item with ID {inv_id} not found."
        )
    
    result = repo.adjust_stock(inv_id, amount)
    
    if not result or not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to adjust inventory stock."
        )
    
    # Return the updated inventory item
    updated_inventory = repo.get_by_id(inv_id)
    if not updated_inventory:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to retrieve updated inventory item."
        )
    
    return updated_inventory


@router.put(
    "/{inv_id}", 
    response_model=Inventory, 
    summary="Manually update an existing inventory item"
)
def update_inventory(
    inv_id: int, 
    inventory_data: InventoryUpdate,  # Validates the incoming partial JSON payload
    repo: InventoryRepository = Depends(get_inventory_repository)
):
    """
    Manually updates an inventory item's properties (name, stock, uom, reorder threshold).
    - Fields not specified in the payload remain untouched.
    """
    # 1. Check if the target inventory record even exists
    if not repo.get_by_id(inv_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Inventory item with ID {inv_id} does not exist."
        )
        
    
    # Optional guard: prevent empty database hits
    if not inventory_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided for update."
        )
        
    # 3. Fire the update directly into the database repo
    updated_records = repo.update(inv_id, inventory_data)
    
    if not updated_records:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update inventory record."
        )
        
    return updated_records[0]