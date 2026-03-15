# APIRouter is used to group related API endpoints together
# Depends is used for dependency injection (for example: database connection or authentication)
# HTTPException is used to return HTTP errors such as 404 Not Found
from fastapi import APIRouter, Depends, HTTPException

# Session type used for interacting with the database
from sqlalchemy.orm import Session

# get_db is a function that provides a database session
# FastAPI automatically creates and closes the session for each request
from app.database import get_db

# Import schemas used for validating incoming request data
# and formatting outgoing response data
from app.schemas.complaint_schema import ComplaintCreate, ComplaintResponse

# Import the service class that contains the complaint business logic
from app.services.complaint_service import ComplaintService

# Import authentication dependency that returns the currently logged-in user
from app.dependencies.auth_dependency import get_current_user

# Import service responsible for complaint verification logic
from app.services.complaint_verification_service import ComplaintVerificationService


# Import authentication dependency again (duplicate import in the original code)
from app.dependencies.auth_dependency import get_current_user

# List type used when returning multiple complaints
from typing import List

# UUID type used for complaint IDs
from uuid import UUID


# Create a router object
# prefix="/complaints" means all routes in this file will start with /complaints
# tags=["Complaints"] groups these endpoints under "Complaints" in Swagger documentation
router = APIRouter(prefix="/complaints", tags=["Complaints"])


# ----------------------------------------
# POST /complaints
# Create a new complaint
# ----------------------------------------
@router.post("/", response_model=ComplaintResponse)
def create_complaint(
    # Request body automatically validated using ComplaintCreate schema
    data: ComplaintCreate,

    # Gets the currently authenticated user from authentication dependency
    user = Depends(get_current_user),

    # Gets a database session from dependency
    db: Session = Depends(get_db)
):

    # Create an instance of the complaint service and pass the database session
    service = ComplaintService(db)

    # Call the service method to create the complaint
    # user["user_id"] is used to associate the complaint with the logged-in user
    complaint = service.create_complaint(data, user["user_id"])

    # Return the created complaint
    # FastAPI converts the returned SQLAlchemy object into ComplaintResponse schema
    return complaint




# ----------------------------------------
# GET /complaints
# Get all complaints
# ----------------------------------------
@router.get("/", response_model=List[ComplaintResponse])
def get_all_complaints(db: Session = Depends(get_db)):

    # Create service object
    service = ComplaintService(db)

    # Return all complaints from the database
    return service.get_all_complaints()


# ----------------------------------------
# GET /complaints/{complaint_id}
# Get one complaint by ID
# ----------------------------------------
@router.get("/{complaint_id}", response_model=ComplaintResponse)

def get_complaint(complaint_id: UUID, db: Session = Depends(get_db)):

    # Create service object
    service = ComplaintService(db)

    # Ask service to find complaint by ID
    complaint = service.get_complaint_by_id(complaint_id)

    # If complaint does not exist, return HTTP 404 error
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Return complaint if found
    return complaint


# ----------------------------------------
# POST /complaints/{complaint_id}/verify
# Citizen verifies whether a complaint is fixed or not
# ----------------------------------------
@router.post("/{complaint_id}/verify")
def verify_complaint(
    # ID of the complaint being verified
    complaint_id: str,

    # Boolean value sent by the user
    # True = issue is fixed
    # False = issue still exists
    is_fixed: bool,

    # Get currently logged-in user
    user = Depends(get_current_user),

    # Get database session
    db: Session = Depends(get_db)
):

    # Create verification service
    service = ComplaintVerificationService(db)

    # Call verification service method
    # Pass complaint_id, current user ID, and verification result
    return service.verify_complaint(
        complaint_id,
        user["user_id"],
        is_fixed
    )