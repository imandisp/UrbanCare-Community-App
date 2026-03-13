from fastapi import FastAPI
from app.routes import auth_routes

from app.models.user import User
from app.models.location import Location
from app.models.complaint import Complaint
from app.models.complaint_image import ComplaintImage

app = FastAPI()

app.include_router(auth_routes.router)