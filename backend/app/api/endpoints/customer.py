# backend/app/api/endpoints/customer.py
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import  Client
from typing import List

from model.customer import Customer, CustomerCreate
from repository.customer_repo import CustomerRepository
from app.db.supabase_client import supabase

def get_supabase():
    """Returns the globally initialized supabase client."""
    return supabase

def get_customer_repository(supabase: Client = Depends(get_supabase)) -> CustomerRepository:
    """Provides an instance of the CustomerRepository with the database connection injected."""
    return CustomerRepository(supabase)

# Define the router instead of importing app
router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

# Change @app to @router, and trim the paths since the prefix handles "/customers"
@router.post(
    "", 
    response_model=Customer, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer"
)

def create_customer(
    customer_in: CustomerCreate, 
    repo: CustomerRepository = Depends(get_customer_repository)
):
    if repo.is_email_taken(customer_in.CUST_EMAIL):
        raise HTTPException(status_code=400, detail="Email address already registered.")
    if repo.is_phone_registered(customer_in.CUST_CONT_NO):
        raise HTTPException(status_code=400, detail="Contact number already registered.")
    return repo.create(customer_in)


@router.get(
    "", 
    response_model=List[Customer], 
    summary="Retrieve all customers"
)
def get_all_customers(repo: CustomerRepository = Depends(get_customer_repository)):
    return repo.get_all()


@router.get(
    "/{customer_id}", 
    response_model=Customer, 
    summary="Get customer by ID"
)
def get_customer_by_id(
    customer_id: int, 
    repo: CustomerRepository = Depends(get_customer_repository)
):
    customer = repo.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer


@router.put(
    "/{customer_id}", 
    response_model=Customer, 
    summary="Update an existing customer"
)
def update_customer(
    customer_id: int, 
    customer_data: Customer, 
    repo: CustomerRepository = Depends(get_customer_repository)
):
    if not repo.get_by_id(customer_id):
        raise HTTPException(status_code=404, detail="Customer does not exist.")
    updated_records = repo.update(str(customer_id), customer_data)
    return updated_records[0]


@router.delete(
    "/{customer_id}", 
    summary="Delete a customer"
)
def delete_customer(
    customer_id: int, 
    repo: CustomerRepository = Depends(get_customer_repository)
):
    if not repo.get_by_id(customer_id):
        raise HTTPException(status_code=404, detail="Customer not found.")
    repo.delete(str(customer_id))
    return {"message": f"Customer {customer_id} has been permanently deleted."}