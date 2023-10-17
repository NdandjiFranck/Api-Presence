# Import du framework
from fastapi import FastAPI

# Documentation
from Documentation.description import api_description
from Documentation.tags import tags_metadata

#Routers
import Routers.router_students
# Initialisation de l'API
app = FastAPI(
    title="Attendance Tracker",
    description=api_description,
    openapi_tags= tags_metadata
)

# Router dédié aux Students
app.include_router(Routers.router_students.router)

# Reste à faire 
# X Sortir mon student's router dans un dossier "routers"
# X Rédiger une documentation et l'ajouter à mon app FastAPI()
# X Sortir mes pydantic models dans un dossier classes
# X Ajouter les tags 


# X et description pour chaque endpoing/methods
# -> En ajouter enpoints suivant en fonction de votre projet


