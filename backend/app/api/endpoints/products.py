# backend/app/api/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from supabase import Client


from app.model.products import Product, ProductCreate, ProductUpdate
from app.repository.product_repo import ProductRepository
from app.db.supabase_client import supabase
from app.repository.bom_repo import BOMRepository
from app.repository.inventory_repo import InventoryRepository
from app.repository.cart_repo import CartRepository
from app.service.supply_chain_service import SupplyChainService # Adjust import path if needed

def get_supabase():
    """Returns the globally initialized supabase client."""
    return supabase

def get_bom_repository(supabase: Client = Depends(get_supabase)) -> BOMRepository:
    return BOMRepository(supabase)

def get_inventory_repository(supabase: Client = Depends(get_supabase)) -> InventoryRepository:
    return InventoryRepository(supabase)

def get_cart_repository(supabase: Client = Depends(get_supabase)) -> CartRepository:
    return CartRepository(supabase)

def get_supply_chain_service(
    bom_repo: BOMRepository = Depends(get_bom_repository),
    inventory_repo: InventoryRepository = Depends(get_inventory_repository),
    cart_repo: CartRepository = Depends(get_cart_repository)
) -> SupplyChainService:
    """Provides an instance of SupplyChainService with all required repos injected."""
    return SupplyChainService(bom_repo, inventory_repo, cart_repo)


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
    repo: ProductRepository = Depends(get_product_repository),
    supply_chain_service: SupplyChainService = Depends(get_supply_chain_service)
):
    """
    Retrieves products. Supports filtering by availability and fuzzy name search.
    - If `search` is provided: Filters products starting with that name string.
    - If `available_only` is true: Filters out unavailable products.
    - If no parameters: Returns all products.
    """
    # Step 1: Fetch the products based on the query parameters
    if search:
        response = repo.search_product_by_name(search)
        products = [Product.model_validate(row) for row in response.data]
        
    elif available_only:
        response = repo.get_available_product()
        products = [Product.model_validate(row) for row in response.data]
        
    else:
        raw_data = repo.get_all()
        # Ensuring rows are Pydantic models even if get_all() returns raw dicts
        products = [
            Product.model_validate(row) if isinstance(row, dict) else row 
            for row in raw_data
        ]
        
    # Step 2: Run live inventory checks across your fetched products
    for product in products:
        is_short = supply_chain_service.update_availability(product.prod_id)
        # If any ingredient is short (True), then availability is False
        product.prod_available = not is_short
        
    # Step 3: Post-filter the list if the user specifically requested available_only.
    # This weeds out items that just failed the live stock check despite what the DB said.
    if available_only:
        products = [p for p in products if p.prod_available]
        
    return products


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
    product_data: ProductUpdate, 
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
        
    updated_records = repo.update(product_id, product_data)
    
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
        
    repo.delete(product_id)
    return {"message": f"Product {product_id} has been permanently deleted."}