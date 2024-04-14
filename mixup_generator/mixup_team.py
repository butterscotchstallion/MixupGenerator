from typing import Required, TypedDict, Unpack

from mixup_generator.mixup_team_member import MixupTeamMember


class MixupTeamKeywords(TypedDict):
    name: Required[str]
    members: Required[set[MixupTeamMember]]


class MixupTeam:
    def __init__(self, **kwargs: Unpack[MixupTeamKeywords]):
        self.name = kwargs["name"]
        self.members = kwargs["members"]

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return self.name
