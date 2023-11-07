import datetime
from pydantic import BaseModel

class Player(BaseModel):
    id: str
    name: str
    club: str
    division: str

class Affiliation(BaseModel):
    id:str
    player_id:str
    team_id:str
    present: bool

class PlayerNoID(BaseModel):
    name: str
    club: str
    division: str

class User(BaseModel):
    email: str
    password: str  