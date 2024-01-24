import json
from classes.schema import Player
from fastapi.testclient import TestClient
from firebase_admin import auth
from database.firebase import authPlayer
from httpx import AsyncClient
import pytest
from main import app  
 
client = TestClient(app)
 
@pytest.fixture
def cleanup(request):
    def remove_test_users():
        # Récupère tous les utilisateurs via l'API d'authentification
        users = auth.list_users().iterate_all()
        
        # Parcours tous les utilisateurs
        for user in users:
            # Vérifie si l'e-mail de l'utilisateur commence par "test_"
            if user.email.startswith("test_"):
                # Supprime l'utilisateur
                auth.delete_user(user.uid)

    # Ajoute la fonction remove_test_users en tant que finalizer
    request.addfinalizer(remove_test_users)

 
 
def test_get_all_players(cleanup):
    # Crée un utilisateur de test en s'inscrivant
    client.post("/auth/signup", json={"email": "test_franck@example.com", "password": "testpassword"})

    # Authentifie l'utilisateur de test et obtient le jeton d'authentification
    auth_token = authPlayer.sign_in_with_email_and_password(email="test_franck@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Envoie une requête GET pour récupérer tous les players avec l'en-tête d'authentification
    response = client.get("/players/", headers=auth_headers)

    # Vérifie si le code de réponse est égal à 200 (OK)
    assert response.status_code == 200

 
def test_add_new_player(cleanup):
    # Crée un utilisateur de test en s'inscrivant
    client.post("/auth/signup", json={"email": "test_franck@example.com", "password": "testpassword"})

    # Authentifie l'utilisateur de test et obtient le jeton d'authentification
    auth_token = authPlayer.sign_in_with_email_and_password(email="test_franck@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Données du player à ajouter
    player_data = {
        "name": "franck",
        "date_of_birt": "12/02/2002",
        "weight": "70kg",
        "height": "180cm",
        "strong_arm": "droit",
        "position_held": "ailier",
        "club": "psg",
        "division": "N2"
    }

    # Envoie une requête POST pour ajouter un nouveau player avec les données du player
    response = client.post("/players/", headers=auth_headers, json=player_data)

    # Affiche la réponse JSON obtenue pour le débogage
    print(response.json())

    # Vérifie si le code de réponse est égal à 201 (Créé)
    assert response.status_code == 201

    # Obtient les données du player nouvellement ajouté
    nouveau_player = response.json()

    # Vérifie si les données du player correspondent aux données fournies
    assert nouveau_player["name"] == player_data["name"]
    assert nouveau_player["date_of_birt"] == player_data["date_of_birt"]
    assert nouveau_player["weight"] == player_data["weight"]
    assert nouveau_player["height"] == player_data["height"]
    assert nouveau_player["strong_arm"] == player_data["strong_arm"]
    assert nouveau_player["position_held"] == player_data["position_held"]
    assert nouveau_player["club"] == player_data["club"]
    assert nouveau_player["division"] == player_data["division"]

 
def test_get_player_id(cleanup):
    # Crée un utilisateur de test en s'inscrivant
    client.post("/auth/signup", json={"email": "test_user@example.com", "password": "testpassword"})
    
    # Authentifie l'utilisateur de test et obtient le jeton d'authentification
    auth_token = authPlayer.sign_in_with_email_and_password(email="test_user@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}
      
    # Données du player à ajouter
    player_data = {
        "name": "franck",
        "date_of_birt": "12/02/2002",
        "weight": "70kg",
        "height": "180cm",
        "strong_arm": "droit",
        "position_held": "ailier",
        "club": "psg",
        "division": "N2"
    }
    
    # Envoie une requête POST pour ajouter un nouveau player avec les données du player
    response = client.post("/players/", headers=auth_headers, json=player_data)
    
    # Vérifie si le code de réponse est égal à 201 (Créé)
    assert response.status_code == 201
    
    # Récupère l'identifiant du player nouvellement ajouté depuis la réponse JSON
    player_id = response.json()["id"]
    
    # Envoyer une requête GET pour obtenir les détails du player en utilisant son identifiant
    response = client.get(f"/players/{player_id}", headers=auth_headers)
    
    # Afficher la réponse JSON obtenue pour le débogage
    print(response.json())
  
    # Vérifier si le code de réponse est égal à 200 (OK)
    assert response.status_code == 200


     
def test_delete_player_id(cleanup):
    # Crée un utilisateur de test en s'inscrivant
    client.post("/auth/signup", json={"email": "test_user@example.com", "password": "testpassword"})
    auth_token = authPlayer.sign_in_with_email_and_password(email="test_user@example.com", password="testpassword")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Données du player à ajouter
    player_data = {
        "name": "franck",
        "date_of_birt": "12/02/2002",
        "weight": "70kg",
        "height": "180cm",
        "strong_arm": "droit",
        "position_held": "ailier",
        "club": "psg",
        "division": "N2"
    }
    
    # Envoie une requête POST pour ajouter un nouveau player avec les données du player
    response = client.post("/players/", headers=auth_headers, json=player_data)
    
    # Vérifie si le code de réponse est égal à 201 (Créé)
    assert response.status_code == 201
    
    # Récupère l'identifiant du player nouvellement ajouté depuis la réponse JSON
    player_id = response.json()["id"]

    # Envoie une requête DELETE pour supprimer le player en utilisant son identifiant
    response = client.delete(f"/players/{player_id}", headers=auth_headers)
    
    # Vérifier si le code de réponse est égal à 204 (Aucun contenu)
    assert response.status_code == 204
