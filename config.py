DB_USER = "postgres"
DB_PASSWORD = "sudhestna"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ragdb"

CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


EMBED_MODEL = "nomic-embed-text"
COLLECTION_NAME = ""


doc_map={"Security Policy":"25e40365-ab3b-4014-9327-031c204c2410",
"HR Policy":"c2e4d34c-0ccf-4777-8401-34cb5db4fd1e",
"Operational Policy":"1a02be65-cc3d-4b4a-a6e7-a36c6769bb1d",
"WorkPlace Policy":"f0f6953b-e5fa-452c-8468-a8a05831dc86"}
        