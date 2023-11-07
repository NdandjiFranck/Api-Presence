import firebase_admin
from firebase_admin import credentials
import pyrebase
from configs.firebase_config import firebaseConfig
 
if not firebase_admin._apps:
    cred = credentials.Certificate("configs/firebasekey.json")
    firebase_admin.initialize_app(cred)
 
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
authPlayer = firebase.auth()