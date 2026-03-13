from fastapi import FastAPI

from app.routes import auth_routes
from app.routes import geofence_routes

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(geofence_routes.router)