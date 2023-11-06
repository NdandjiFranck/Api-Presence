# Import du framework
from fastapi import FastAPI

# Documentation
from documentations.description import api_description
from documentations.tags import tags_metadata

#Routers
import routers.router_students
import routers.router_cours
import routers.router_auth
# Initialisation de l'API
app = FastAPI(
    title="Attendance Tracker",
    description=api_description,
    openapi_tags= tags_metadata
)

# Router dédié aux Students
app.include_router(routers.router_students.router)
app.include_router(routers.router_cours.router)
app.include_router(routers.router_auth.router)

