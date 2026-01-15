import os
from pymongo import MongoClient

# ---------- MondoDB ----------

# helper for create client
def create_mongo_client():
    """
    Retunrs the db with name assigned
        loads envs
        makes db uri
        creates client
        names the db 
    """
    host = os.getenv("MONGO_HOST", "localhost") # in yaml -> mongo-0.mongo
    port = int(os.getenv("MONGO_PORT", "27017"))
    username = os.getenv("MONGO_USERNAME", "admin")
    password = os.getenv("MONGO_PASSWORD", "secretpass")
    db_name = os.getenv("MONGO_DB", "threat_db")

    # uri = "mongodb://MONGO_USERNAME:MONGO_PASSWORD@MONGO_HOST:MONGO_PORT"
    uri = f"mongodb://{username}:{password}@{host}:{port}"

    client = MongoClient(uri)

    mongo_db = client[db_name]

    return mongo_db


# --------- CREATE THE DB --------------------

mongo_db = create_mongo_client()
threats_collection = mongo_db["threats"]

def insert_to_db(threats):
    threats_collection.insert_many(threats)

