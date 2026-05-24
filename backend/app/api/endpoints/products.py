# backend/app/api/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from supabase import Client


from app.model.products import Product, ProductCreate
from app.repository.product_repo import ProductRepository
from app.db.supabase_client import supabase

def get_supabase():
    """Returns the globally initialized supabase client."""
    return supabase

def get_product_repository(supabase: Client = Depends(get_supabase)) -> ProductRepository:
    """Provides an instance of the CustomerRepository with the database connection injected."""
    return ProductRepository(supabase)

# Define the router instead of importing app
router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post(
    "", 
    response_model=Product, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer"
)

@router.post(
    "", 
    response_model=Product, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product"
)
def create_product(
    product_in: ProductCreate, 
    repo: ProductRepository = Depends(get_product_repository)
):
    """
    Creates a new product record.
    """
    # Uses inherited BaseRepository.create()
    return repo.create(product_in)


@router.get(
    "", 
    response_model=List[Product], 
    summary="Retrieve products"
)
def get_products(
    available_only: bool = False,
    search: Optional[str] = None,
    repo: ProductRepository = Depends(get_product_repository)
):
    """
    Retrieves products. Supports filtering by availability and fuzzy name search.
    - If `search` is provided: Filters products starting with that name string.
    - If `available_only` is true: Filters out unavailable products.
    - If no parameters: Returns all products.
    """
    # Case A: Name Search takes priority
    if search:
        response = repo.search_product_by_name(search)
        return [
            Product.model_validate(row)
            for row in response.data]
        
    # Case B: Filter by availability
    if available_only:
        response = repo.get_available_product()
        return [
            Product.model_validate(row)
            for row in response.data
            ]
        
    # Case C: Fallback to all products
    return repo.get_all()


@router.get(
    "/{product_id}", 
    response_model=Product, 
    summary="Get product by ID"
)
def get_product_by_id(
    product_id: int, 
    repo: ProductRepository = Depends(get_product_repository)
):
    """
    Retrieves a single product using its primary key ID.
    """
    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Product with ID {product_id} not found."
        )
    return product


@router.put(
    "/{product_id}", 
    response_model=Product, 
    summary="Update an existing product"
)
def update_product(
    product_id: int, 
    product_data: Product, 
    repo: ProductRepository = Depends(get_product_repository)
):
    """
    Updates an entire product profile.
    """
    if not repo.get_by_id(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Product with ID {product_id} does not exist."
        )
        
    updated_records = repo.update(str(product_id), product_data)
    
    if not updated_records:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update product record."
        )
        
    return updated_records[0]


@router.delete(
    "/{product_id}", 
    summary="Delete a product"
)
def delete_product(
    product_id: int, 
    repo: ProductRepository = Depends(get_product_repository)
):
    """
    Deletes a product record permanently from the database.
    """
    if not repo.get_by_id(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Product with ID {product_id} not found."
        )
        
    repo.delete(str(product_id))
    return {"message": f"Product {product_id} has been permanently deleted."}