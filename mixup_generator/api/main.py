import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine, select

from mixup_generator.api.models import Team, TeamTeamMembersLink

logging.basicConfig()
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.DEBUG)

engine = create_engine("sqlite:///./database.db", echo=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating all tables")
    SQLModel.metadata.create_all(engine)
    # Everything before yield is before the app starts
    yield
    # After the yield is after the app has started


app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def select_teams():
    with Session(engine) as session:
        statement = select(Team).where(Team.active)
        results = session.exec(statement)
        if results:
            return results.all()
        else:
            return []


def select_team_members():
    with Session(engine) as session:
        statement = (
            select(TeamTeamMembersLink)
            .where(Team.active)
            .group_by(text("team_member_id"))
        )

        results = session.exec(statement)
        if results:
            return results.all()
        else:
            return []


## Routes


@app.get("/api/teams")
async def teams_list():
    return {"teams": select_teams()}


@app.get("/api/team-members")
async def team_members_list():
    return {"team_members": select_team_members()}
