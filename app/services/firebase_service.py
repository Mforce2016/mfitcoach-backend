import firebase_admin
import os
import json
from firebase_admin import credentials
from firebase_admin import firestore

firebase_json = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_json:

    raise Exception(
        "FIREBASE_CREDENTIALS no encontrada"
    )

cred_dict = json.loads(firebase_json)

cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)

db = firestore.client()