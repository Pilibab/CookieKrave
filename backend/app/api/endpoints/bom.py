# backend/app/api/endpoints/bom.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client

from app.model.bom import Bom, BomCreate, BomUpdate
from app.repository.bom_repo import BOMRepository
from app.db.supabase_client import supabase

def get_supabase():
    """Returns the globally initialized supabase client."""
    return supabase

def get_bom_repository(supabase: Client = Depends(get_supabase)) -> BOMRepository:
    """Provides an instance of the BOMRepository with the database connection injected."""
    return BOMRepository(supabase)

# Define the router
router = APIRouter(
    prefix="/bom",
    tags=["bom"],
)

@router.post(
    "", 
    response_model=Bom, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new BOM entry"
)
def create_bom(
    bom_in: BomCreate, 
    repo: BOMRepository = Depends(get_bom_repository)
):
    """
    Creates a new Bill of Materials entry linking a product to an ingredient.
    """
    return repo.create(bom_in)


@router.get(
    "", 
    response_model=List[Bom], 
    summary="Retrieve all BOM entries"
)
def get_all_bom(
    repo: BOMRepository = Depends(get_bom_repository)
):
    """
    Retrieves all Bill of Materials entries.
    """
    bom_entries = repo.get_all()
    return bom_entries if bom_entries else []

@router.get(
    "/{bom_id}", 
    response_model=Bom, 
    summary="Get BOM entry by ID"
)
def get_bom_by_id(
    bom_id: int, 
    repo: BOMRepository = Depends(get_bom_repository)
):
    """
    Retrieves a single BOM entry by its ID.
    """
    bom = repo.get_by_id(bom_id)
    if not bom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"BOM entry with ID {bom_id} not found."
        )
    return bom


@router.get(
    "/product/{product_id}", 
    response_model=List[Bom], 
    summary="Get ingredients for a product"
)
def get_stock_for_product(
    product_id: int, 
    repo: BOMRepository = Depends(get_bom_repository)
):
    """
    Retrieves all ingredients and quantities required to make a specific product.
    """
    stock = repo.get_stock(product_id)
    # if not stock:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, 
    #         detail=f"No ingredients found for product {product_id}."
    #     )
    return stock if stock else []


@router.get(
    "/ingredient/{inventory_id}", 
    response_model=List[Bom], 
    summary="Get products using an ingredient"
)
def get_products_using_ingredient(
    inventory_id: int, 
    repo: BOMRepository = Depends(get_bom_repository)
):
    """
    Finds all products that use a specific inventory item/ingredient.
    """
    products = repo.get_products_using_ingredient(inventory_id)
    # if not products:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, 
    #         detail=f"No products found using ingredient {inventory_id}."
    #     )
    return products if products else []


@router.put(
    "/{bom_id}", 
    response_model=Bom, 
    summary="Update a BOM entry"
)
def update_bom(
    bom_id: int, 
    bom_data: BomUpdate, 
    repo: BOMRepository = Depends(get_bom_repository)
):
    """
    Updates a Bill of Materials entry.
    """
    if not repo.get_by_id(bom_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"BOM entry with ID {bom_id} does not exist."
        )
        
    updated_records = repo.update(str(bom_id), bom_data)
    
    if not updated_records:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update BOM entry."
        )
        
    return updated_records[0]


@router.delete(
    "/{bom_id}", 
    summary="Delete a BOM entry"
)
def delete_bom(
    bom_id: int, 
    repo: BOMRepository = Depends(get_bom_repository)
):
    """
    Deletes a Bill of Materials entry.
    """
    if not repo.get_by_id(bom_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"BOM entry with ID {bom_id} not found."
        )
        
    repo.delete(str(bom_id))
    return {"message": f"BOM entry {bom_id} has been permanently deleted."}
