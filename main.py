# Import du framework
from fastapi import FastAPI

# Documentation
from documentations.description import api_description
from documentations.tags import tags_metadata

#Routers
import routers.router_players
#import routers.router_teams
import routers.router_auth
# Initialisation de l'API
app = FastAPI(
    title="Players Affiliation",
    description=api_description,
    openapi_tags= tags_metadata
)

# Router dédié aux players
app.include_router(routers.router_players.router)
#app.include_router(routers.router_teams.router)
app.include_router(routers.router_auth.router)

