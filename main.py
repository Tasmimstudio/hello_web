from fastapi import FastAPI
from neomodel import config, StructuredNode, StringProperty, RelationshipTo, UniqueIdProperty
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Neo4j configuration
config.DATABASE_URL = os.getenv("NEO4J_BOLT_URL", "bolt://neo4j:your_password_here@localhost:7687")

# Neo4j Models
class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    age = StringProperty()

@app.get("/")
def read_root():
    return {"HELLO WEB"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/persons/")
def create_person(name: str, age: str = None):
    person = Person(name=name, age=age).save()
    return {"uid": person.uid, "name": person.name, "age": person.age}

@app.get("/persons/")
def get_all_persons():
    persons = Person.nodes.all()
    return [{"uid": p.uid, "name": p.name, "age": p.age} for p in persons]

@app.get("/test-neo4j")
def test_neo4j_connection():
    try:
        # Try to connect and run a simple query
        from neomodel import db
        results, meta = db.cypher_query("RETURN 'Connection successful' as message")
        return {"status": "connected", "message": results[0][0]}
    except Exception as e:
        return {"status": "error", "message": str(e)}