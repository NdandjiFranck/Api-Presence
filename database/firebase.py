import firebase_admin
from configs.firebase_config import firebaseConfig
import pyrebase

if not firebase_admin._apps :
    cred = firebase_admin.credentials.Certificate("configs/api-presence-firebase-adminsdk-4lxbg-89bb07eb0b.json")
    firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

#authentication
authStudent = firebase.auth()