from pydantic import BaseModel

# Model Pydantic = Datatype
class Player(BaseModel):
    id: str
    name: str

class PlayerNoID(BaseModel):
    name: str