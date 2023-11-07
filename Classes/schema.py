import datetime
from pydantic import BaseModel

class Player(BaseModel):
    id: str
    name: str

class Team(BaseModel):
    id: str
    name: str
    club:str
    date_heure:str

class Attendance(BaseModel):
    id:str
    player_id:str
    team_id:str
    present: bool

class PlayerNoID(BaseModel):
    name: str

class User(BaseModel):
    email: str
    password: str  