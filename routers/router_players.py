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
    Player(id="player1", name="Franck", date_of_birt= "04/11/19998", weight= "1.80kg", height= "190cm", strong_arm= "droite", position_held= "ailier", club="Us Ivry", division= "N1"),
    Player(id="player2", name="Salif", date_of_birt= "15/02/2000", weight= "1.89kg", height= "185cm", strong_arm= "gauche", position_held= "gb", club="Tremblay Hb", division= "D2"),
    Player(id="player3", name="Moas", date_of_birt= "09/07/2001", weight= "1.70kg", height= "191cm", strong_arm= "droite", position_held= "demi centre", club="Creteil", division= "N1")
]

@router.get('', response_model=List[Player])
async def get_player(userData: int = Depends(get_current_user)):
    """List all the players from a championship"""
    player_InDB =  db.child('player').get().val()
    #db.child("player").get().val()
    resultsarray= []
    if player_InDB:
        for player_id, player_info in player_InDB.items():
            player= Player( **player_info)
            resultsarray.append(player)
    return resultsarray

@router.get('/{player_id}', response_model=Player)
async def get_player_by_id(player_id: str, userData: int = Depends(get_current_user)):
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
          date_of_birt= givePlayer.date_of_birt,
          weight= givePlayer.weight,
          height= givePlayer.height,
          strong_arm= givePlayer.strong_arm,
          position_held= givePlayer.position_held,
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
        "date_of_birt": modifiedPlayer.date_of_birt,
        "weight": modifiedPlayer.weight,
        "height": modifiedPlayer.height,
        "strong_arm": modifiedPlayer.strong_arm,
        "position_held": modifiedPlayer.position_held,
        "club": modifiedPlayer.club,
        "division": modifiedPlayer.division
    }
    if not userData: 
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    onePlayer_InDB = db.child("player").child(player_id).get().val()
    if onePlayer_InDB is None:
        raise HTTPException(status_code= 404, detail="Player not found")
    after_update= db.child("player").child(player_id).update(updatePlayer)
    return after_update

@router.delete('/{player_id}', status_code=204)
async def delete_player(player_id:str, userData: int = Depends(get_current_user)):
    onePlayer_InDB = db.child("player").child(player_id).get().val()
    if onePlayer_InDB is None:
        raise HTTPException(status_code= 404, detail="Player not found")
    after_delete= db.child("player").child(player_id).remove()
    return None