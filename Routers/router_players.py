from fastapi import APIRouter,Depends, HTTPException
from typing import List
import uuid
from classes.schema import Player, PlayerNoID
from database.firebase import db
from routers.router_auth import get_current_user


router= APIRouter(
    prefix='/players',
    tags=["players"]
)

players = [
    Player(id="player1", name="Adama", club="Us Ivry", division= "N1"),
    Player(id="player2", name="Adrien", club="Tremblay Hb", division= "D2"),
    Player(id="player3", name="Akbar", club="Creteil", division= "N1")
]

@router.get('', response_model=List[Player])
async def get_player():
    """List all the players from a  championship (context fonctionnel ou technique)"""
    player_InDB =  db.child('player').get().val()
    #db.child("player").get().val()
    resultsarray= []
    if player_InDB:
        for player_id, player_info in player_InDB.items():
            player= Player( **player_info)
            resultsarray.append(player)
    return resultsarray

@router.get('/{player_id}', response_model=Player)
async def get_player_by_id(player_id: str):
    onePlayer_InDB = db.child("player").child(player_id).get().val()
    if onePlayer_InDB is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    player = Player(**onePlayer_InDB)
    return player

@router.post('', response_model=Player, status_code=201)
async def add_new_player(givePlayer:PlayerNoID, userData: int = Depends(get_current_user)):
    generatedId= uuid.uuid4()
    newPlayer= Player(
        id=str(generatedId),
          name=givePlayer.name, 
          club=givePlayer.club, 
          division=givePlayer.division
          )
    players.append(newPlayer)

    #connexion à la base de donnée
    db.child("player").child(str(generatedId)).set(newPlayer.model_dump())
    if not userData: 
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return newPlayer

@router.patch('/{player_id}', status_code=204)
async def modify_player(player_id:str, modifiedPlayer: PlayerNoID, userData: int = Depends(get_current_user)):
    #CONNEXION TO DATA BASE
    updatePlayer = {
        "name": modifiedPlayer.name,
        "club": modifiedPlayer.club,
        "division": modifiedPlayer.division
    }
    onePlayer_InDB = db.child("player").child(player_id).get().val()
    if onePlayer_InDB is None:
        raise HTTPException(status_code= 404, detail="Player not found")
    after_update= db.child("player").child(player_id).update(updatePlayer)
    return after_update

@router.delete('/{player_id}', status_code=204)
async def delete_player(player_id:str):
    onePlayer_InDB = db.child("player").child(player_id).get().val()
    if onePlayer_InDB is None:
        raise HTTPException(status_code= 404, detail="Player not found")
    after_delete= db.child("player").child(player_id).remove()
    return None


