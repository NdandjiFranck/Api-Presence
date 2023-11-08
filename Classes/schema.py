import datetime
from pydantic import BaseModel

class Player(BaseModel):
    id: str
    name: str
    date_of_birt: str
    weight: str
    height: str
    strong_arm: str
    position_held: str
    club: str
    division: str

class Affiliation(BaseModel):
    id:str
    player_id:str
    #team_id:str
    present: bool

class PlayerNoID(BaseModel):
    name: str
    date_of_birt: str
    weight: str
    height: str
    strong_arm: str
    position_held: str
    club: str
    division: str

class User(BaseModel):
    email: str
    password: str  