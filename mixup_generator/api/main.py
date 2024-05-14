import logging
from contextlib import asynccontextmanager

import sqlalchemy
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine, select

from mixup_generator.api.models import Team, TeamMember, TeamTeamMembersLink

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
        statement = select(TeamMember).where(TeamMember.active)
        results = session.exec(statement)
        if results:
            return results.all()
        else:
            return []


def select_team_member_team_link():
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


## Teams
@app.get("/api/teams")
async def teams_route():
    return {"teams": select_teams()}


@app.post("/api/teams")
async def teams_create_route(team: Team):
    status = "ERROR"
    message = None
    try:
        team_name = team.name.strip()
        if team_name and len(team_name) > 0 and len(team_name) <= 50:
            with Session(engine) as session:
                session.add(Team(name=team_name))
                session.commit()
            status = "OK"
            message = "Team created"
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Team name exists")

    return {"status": status, "message": message}


## Team Members
@app.get("/api/team-members")
async def team_members_route():
    return {"team_members": select_team_members()}


## Team Member links
@app.get("/api/team-member-team-link")
async def team_member_team_link_route():
    return {"team_member_team_link": select_team_member_team_link()}
