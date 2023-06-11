from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import find_dotenv, load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from notion_ngrok_chat import create_db_from_notion, get_response_from_query
from fastapi.middleware.cors import CORSMiddleware


# Initialize FastAPI app
app = FastAPI()

load_dotenv(find_dotenv())
embeddings = OpenAIEmbeddings()

class Database(BaseModel):
    notion_token: str
    database_id: str

class Query(BaseModel):
    notion_token: str
    database_id: str
    question: str

# In-memory dictionary to store db objects for different Notion databases.
db_dict = {}

origins = [
    "http://localhost:3000", #change later after testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create_db")
async def create_db(data: Database):
    db = create_db_from_notion(data.notion_token, data.database_id)
    # Storing db in our in-memory dictionary
    db_dict[(data.notion_token, data.database_id)] = db
    return {
        "message": "Database created successfully",
    }

@app.post("/get_response")
async def get_response(query: Query):
    # Fetching the db object from our in-memory dictionary.
    db = db_dict.get((query.notion_token, query.database_id))
    if not db:
        return {"error": "Database not found."}
    response, docs = get_response_from_query(db, query.question)

    # Assuming docs are list of strings
    return {
        "response": response,
        "docs": [str(doc) for doc in docs],
    }
