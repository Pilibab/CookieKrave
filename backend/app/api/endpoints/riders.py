# backend/app/api/endpoints/riders.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client


from model.rider import Rider, RiderCreate
from repository.rider_repo import RiderRepository
from app.db.supabase_client import supabase

def get_supabase():
    """Returns the globally initialized supabase client."""
    return supabase

def get_rider_repository(supabase: Client = Depends(get_supabase)) -> RiderRepository:
    """Provides an instance of the RiderRepository with the database connection injected."""
    return RiderRepository(supabase)

# Define the router
router = APIRouter(
    prefix="/riders",
    tags=["riders"]
)

@router.post(
    "", 
    response_model=Rider, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new rider"
)
def create_rider(
    rider_in: RiderCreate, 
    repo: RiderRepository = Depends(get_rider_repository)
):
    """
    Creates a new rider record.
    """
    return repo.create(rider_in)


@router.get(
    "", 
    response_model=List[Rider], 
    summary="Retrieve all riders"
)
def get_all_riders(
    repo: RiderRepository = Depends(get_rider_repository)
):
    """
    Retrieves all riders from the database.
    """
    return repo.get_all()


@router.get(
    "/{rider_id}", 
    response_model=Rider, 
    summary="Get rider by ID"
)
def get_rider_by_id(
    rider_id: int, 
    repo: RiderRepository = Depends(get_rider_repository)
):
    """
    Retrieves a single rider using their primary key ID.
    """
    rider = repo.get_by_id(rider_id)
    if not rider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Rider with ID {rider_id} not found."
        )
    return rider


@router.put(
    "/{rider_id}", 
    response_model=Rider, 
    summary="Update an existing rider"
)
def update_rider(
    rider_id: int, 
    rider_data: Rider, 
    repo: RiderRepository = Depends(get_rider_repository)
):
    """
    Updates an entire rider profile.
    """
    if not repo.get_by_id(rider_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Rider with ID {rider_id} does not exist."
        )
        
    updated_records = repo.update(str(rider_id), rider_data)
    
    if not updated_records:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update rider record."
        )
        
    return updated_records[0]


@router.patch(
    "/{rider_id}/location", 
    response_model=Rider, 
    summary="Update rider location"
)
def update_rider_location(
    rider_id: int,
    new_location: str,
    repo: RiderRepository = Depends(get_rider_repository)
):
    """
    Updates a rider's real-time location.
    """
    if not repo.get_by_id(rider_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Rider with ID {rider_id} not found."
        )
    
    result = repo.update_location(rider_id, new_location)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update rider location."
        )
    
    # Return the updated rider
    updated_rider = repo.get_by_id(rider_id)
    if not updated_rider:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to retrieve updated rider."
        )
    
    return updated_rider


@router.delete(
    "/{rider_id}", 
    summary="Delete a rider"
)
def delete_rider(
    rider_id: int, 
    repo: RiderRepository = Depends(get_rider_repository)
):
    """
    Deletes a rider record permanently from the database.
    """
    if not repo.get_by_id(rider_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Rider with ID {rider_id} not found."
        )
        
    repo.delete(str(rider_id))
    return {"message": f"Rider {rider_id} has been permanently deleted."}
