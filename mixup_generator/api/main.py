from fastapi import FastAPI

from mixup_generator.api.database import Database
from mixup_generator.team import Team

app = FastAPI()

db = Database()
engine = db.engine
base = db.base
base.metadata.create_all(bind=engine)


@app.get("/teams")
async def teams_list():
    return {"teams": Team().query.all()}
