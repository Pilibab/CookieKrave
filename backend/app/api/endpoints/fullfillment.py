# backend/app/api/endpoints/fullfillment.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client


from model.fullfillement import (
    Fulfillment, FulfillmentCreate,
    Delivery, DeliveryCreate,
    PickUp, PickUpCreate
)
from repository.fullfillment_repo import (
    FulfillmentRepository,
    DeliveryRepository,
    PickUpRepository
)
from app.db.supabase_client import supabase

def get_supabase():
    """Returns the globally initialized supabase client."""
    return supabase

def get_fulfillment_repository(supabase: Client = Depends(get_supabase)) -> FulfillmentRepository:
    """Provides an instance of the FulfillmentRepository."""
    return FulfillmentRepository(supabase)

def get_delivery_repository(supabase: Client = Depends(get_supabase)) -> DeliveryRepository:
    """Provides an instance of the DeliveryRepository."""
    return DeliveryRepository(supabase)

def get_pickup_repository(supabase: Client = Depends(get_supabase)) -> PickUpRepository:
    """Provides an instance of the PickUpRepository."""
    return PickUpRepository(supabase)

# Define routers
fulfillment_router = APIRouter(
    prefix="/fulfillment",
    tags=["fulfillment"]
)

delivery_router = APIRouter(
    prefix="/delivery",
    tags=["delivery"]
)

pickup_router = APIRouter(
    prefix="/pickup",
    tags=["pickup"]
)

# ==========================================
# FULFILLMENT ENDPOINTS
# ==========================================

@fulfillment_router.post(
    "", 
    response_model=Fulfillment, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new fulfillment"
)
def create_fulfillment(
    fulfillment_in: FulfillmentCreate, 
    repo: FulfillmentRepository = Depends(get_fulfillment_repository)
):
    """
    Creates a new fulfillment record (Delivery or Pick_Up).
    """
    return repo.create(fulfillment_in)


@fulfillment_router.get(
    "", 
    response_model=List[Fulfillment], 
    summary="Retrieve all fulfillments"
)
def get_all_fulfillments(
    repo: FulfillmentRepository = Depends(get_fulfillment_repository)
):
    """
    Retrieves all fulfillment records.
    """
    return repo.get_all()


@fulfillment_router.get(
    "/{fulfillment_id}", 
    response_model=Fulfillment, 
    summary="Get fulfillment by ID"
)
def get_fulfillment_by_id(
    fulfillment_id: int, 
    repo: FulfillmentRepository = Depends(get_fulfillment_repository)
):
    """
    Retrieves a single fulfillment record by ID.
    """
    fulfillment = repo.get_by_id(fulfillment_id)
    if not fulfillment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fulfillment with ID {fulfillment_id} not found."
        )
    return fulfillment


@fulfillment_router.put(
    "/{fulfillment_id}", 
    response_model=Fulfillment, 
    summary="Update a fulfillment"
)
def update_fulfillment(
    fulfillment_id: int, 
    fulfillment_data: Fulfillment, 
    repo: FulfillmentRepository = Depends(get_fulfillment_repository)
):
    """
    Updates a fulfillment record.
    """
    if not repo.get_by_id(fulfillment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fulfillment with ID {fulfillment_id} does not exist."
        )
        
    updated_records = repo.update(str(fulfillment_id), fulfillment_data)
    
    if not updated_records:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update fulfillment record."
        )
        
    return updated_records[0]


@fulfillment_router.delete(
    "/{fulfillment_id}", 
    summary="Delete a fulfillment"
)
def delete_fulfillment(
    fulfillment_id: int, 
    repo: FulfillmentRepository = Depends(get_fulfillment_repository)
):
    """
    Deletes a fulfillment record.
    """
    if not repo.get_by_id(fulfillment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Fulfillment with ID {fulfillment_id} not found."
        )
        
    repo.delete(str(fulfillment_id))
    return {"message": f"Fulfillment {fulfillment_id} has been permanently deleted."}


# ==========================================
# DELIVERY ENDPOINTS
# ==========================================

@delivery_router.post(
    "", 
    response_model=Delivery, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new delivery"
)
def create_delivery(
    delivery_in: DeliveryCreate, 
    repo: DeliveryRepository = Depends(get_delivery_repository)
):
    """
    Creates a new delivery fulfillment record.
    """
    return repo.create(delivery_in)


@delivery_router.get(
    "", 
    response_model=List[Delivery], 
    summary="Retrieve all deliveries"
)
def get_all_deliveries(
    repo: DeliveryRepository = Depends(get_delivery_repository)
):
    """
    Retrieves all delivery records.
    """
    return repo.get_all()


@delivery_router.get(
    "/{fulfillment_id}", 
    response_model=Delivery, 
    summary="Get delivery by fulfillment ID"
)
def get_delivery_by_id(
    fulfillment_id: int, 
    repo: DeliveryRepository = Depends(get_delivery_repository)
):
    """
    Retrieves a delivery record by its fulfillment ID.
    """
    delivery = repo.get_by_id(fulfillment_id)
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Delivery with fulfillment ID {fulfillment_id} not found."
        )
    return delivery


@delivery_router.get(
    "/rider/{rider_id}", 
    response_model=List[Delivery], 
    summary="Get deliveries by rider"
)
def get_deliveries_by_rider(
    rider_id: int, 
    repo: DeliveryRepository = Depends(get_delivery_repository)
):
    """
    Retrieves all delivery tasks assigned to a specific rider.
    """
    deliveries = repo.get_deliveries_by_rider(rider_id)
    if not deliveries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No deliveries found for rider {rider_id}."
        )
    return deliveries


@delivery_router.put(
    "/{fulfillment_id}", 
    response_model=Delivery, 
    summary="Update a delivery"
)
def update_delivery(
    fulfillment_id: int, 
    delivery_data: Delivery, 
    repo: DeliveryRepository = Depends(get_delivery_repository)
):
    """
    Updates a delivery record.
    """
    if not repo.get_by_id(fulfillment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Delivery with fulfillment ID {fulfillment_id} does not exist."
        )
        
    updated_records = repo.update(str(fulfillment_id), delivery_data)
    
    if not updated_records:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update delivery record."
        )
        
    return updated_records[0]


@delivery_router.delete(
    "/{fulfillment_id}", 
    summary="Delete a delivery"
)
def delete_delivery(
    fulfillment_id: int, 
    repo: DeliveryRepository = Depends(get_delivery_repository)
):
    """
    Deletes a delivery record.
    """
    if not repo.get_by_id(fulfillment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Delivery with fulfillment ID {fulfillment_id} not found."
        )
        
    repo.delete(str(fulfillment_id))
    return {"message": f"Delivery {fulfillment_id} has been permanently deleted."}


# ==========================================
# PICK UP ENDPOINTS
# ==========================================

@pickup_router.post(
    "", 
    response_model=PickUp, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new pick up"
)
def create_pickup(
    pickup_in: PickUpCreate, 
    repo: PickUpRepository = Depends(get_pickup_repository)
):
    """
    Creates a new pick up fulfillment record.
    """
    return repo.create(pickup_in)


@pickup_router.get(
    "", 
    response_model=List[PickUp], 
    summary="Retrieve all pick ups"
)
def get_all_pickups(
    repo: PickUpRepository = Depends(get_pickup_repository)
):
    """
    Retrieves all pick up records.
    """
    return repo.get_all()


@pickup_router.get(
    "/{fulfillment_id}", 
    response_model=PickUp, 
    summary="Get pick up by fulfillment ID"
)
def get_pickup_by_id(
    fulfillment_id: int, 
    repo: PickUpRepository = Depends(get_pickup_repository)
):
    """
    Retrieves a pick up record by its fulfillment ID.
    """
    pickup = repo.get_by_id(fulfillment_id)
    if not pickup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Pick up with fulfillment ID {fulfillment_id} not found."
        )
    return pickup


@pickup_router.put(
    "/{fulfillment_id}", 
    response_model=PickUp, 
    summary="Update a pick up"
)
def update_pickup(
    fulfillment_id: int, 
    pickup_data: PickUp, 
    repo: PickUpRepository = Depends(get_pickup_repository)
):
    """
    Updates a pick up record.
    """
    if not repo.get_by_id(fulfillment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Pick up with fulfillment ID {fulfillment_id} does not exist."
        )
        
    updated_records = repo.update(str(fulfillment_id), pickup_data)
    
    if not updated_records:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update pick up record."
        )
        
    return updated_records[0]


@pickup_router.delete(
    "/{fulfillment_id}", 
    summary="Delete a pick up"
)
def delete_pickup(
    fulfillment_id: int, 
    repo: PickUpRepository = Depends(get_pickup_repository)
):
    """
    Deletes a pick up record.
    """
    if not repo.get_by_id(fulfillment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Pick up with fulfillment ID {fulfillment_id} not found."
        )
        
    repo.delete(str(fulfillment_id))
    return {"message": f"Pick up {fulfillment_id} has been permanently deleted."}


# Export all routers
router = [fulfillment_router, delivery_router, pickup_router]
