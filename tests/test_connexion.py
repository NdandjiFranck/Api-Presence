import pytest 
from fastapi.testclient import TestClient
from main import app
from firebase_admin import auth

client = TestClient(app)

@pytest.fixture
def cleanup(request):
    # La fonction remove_test_users est définie à l'intérieur de cleanup et sera utilisée comme finalizer.
    def remove_test_users():
        # Récupère la liste de tous les utilisateurs dans le système d'authentification.
        users = auth.list_users().iterate_all()
        
        # Parcours tous les utilisateurs.
        for user in users:
            # Vérifie si l'adresse e-mail de l'utilisateur commence par "test_".
            if user.email.startswith("test_"):
                # Supprime l'utilisateur du système d'authentification.
                auth.delete_user(user.uid)

    # Ajoute la fonction remove_test_users comme finalizer pour être exécutée à la fin des tests.
    request.addfinalizer(remove_test_users)

# test avec nettoyage
def test_create_account_success(cleanup):
    # Appelle l'API pour créer un nouveau compte utilisateur avec une adresse e-mail et un mot de passe spécifiés.
    response = client.post("/auth/signup", json={"email": "test_franck@example.com", "password": "testpassword"})

    # Vérifie que la réponse de l'API a un code de statut HTTP 201 (Créé avec succès).
    assert response.status_code == 201

    # Vérifie que la réponse JSON de l'API contient la clé "message".
    assert "message" in response.json()

    # Vérifie que la réponse JSON de l'API contient la clé "id" dans le champ "message".
    assert "id" in response.json()["message"]


def test_create_account_conflict(cleanup):
    # Appelle l'API pour tenter de créer un nouveau compte utilisateur avec une adresse e-mail déjà existante.
    response = client.post("/auth/signup", json={"email": "tchtenga23@gmail.com", "password": "123456"})

    # Vérifie que la réponse de l'API a un code de statut HTTP 409 (Conflit) indiquant que la ressource existe déjà.
    assert response.status_code == 409


def test_login(cleanup):
    # Crée un nouveau compte utilisateur en appelant l'API d'inscription.
    response_create = client.post("/auth/signup", json={"email": "test_test@example.com", "password": "testpassword"})
    
    # Vérifie que la création du compte a réussi avec un code de statut HTTP 201 (Créé).
    assert response_create.status_code == 201
    
    # Tente de se connecter en appelant l'API de connexion avec les informations du nouveau compte.
    response_login = client.post("/auth/login", data={"username": "test_test@example.com", "password": "testpassword"})
    
    # Vérifie que la connexion a réussi avec un code de statut HTTP 200 (OK).
    assert response_login.status_code == 200
    
    # Vérifie que la réponse de l'API contient un jeton d'accès ("access_token").
    assert "access_token" in response_login.json()


def test_login_user_not_exists():
    # Tente de se connecter en appelant l'API de connexion avec des informations d'identification incorrectes.
    response = client.post("/auth/login", data={"username": "utilisateur_inconnu@example.com", "password": "mot_de_passe_incorrect"})
    
    # Vérifie que la tentative de connexion échoue avec un code de statut HTTP 401 (Non autorisé).
    assert response.status_code == 401
    
    # Vérifie que le détail de la réponse indique "Invalid Credentials" (Informations d'identification non valides).
    assert "Invalid Credentials" in response.json()["detail"]




