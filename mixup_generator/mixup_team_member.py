from typing import NotRequired, Required, TypedDict, Unpack


class MixupTeamMemberKeywords(TypedDict):
    name: Required[str]
    username: NotRequired[str]


class MixupTeamMember:
    name: str
    username: str

    def __init__(self, **kwargs: Unpack[MixupTeamMemberKeywords]):
        self.name = kwargs["name"]

        if "username" in kwargs:
            self.username = kwargs["username"]
        else:
            self.username = self.generate_default_username(self.name)

    def generate_default_username(self, name: str) -> str:
        username = name
        if " " in name:
            name_parts = name.split()
            username = f"{name_parts[0][0]}{name_parts[-1]}"
        return username.lower()

    def __repr__(self) -> str:
        return self.name
