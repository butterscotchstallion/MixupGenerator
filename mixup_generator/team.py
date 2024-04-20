from typing import Required, TypedDict, Unpack

from mixup_generator.team_member import TeamMember


class TeamKeywords(TypedDict):
    name: Required[str]
    members: Required[set[TeamMember]]


class Team:
    def __init__(self, **kwargs: Unpack[TeamKeywords]):
        self.name = kwargs["name"]
        self.members = kwargs["members"]

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return self.name
