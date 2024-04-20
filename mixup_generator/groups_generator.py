from random import shuffle

from mixup_generator.logger import logger
from mixup_generator.team import Team
from mixup_generator.team_member import TeamMember


class GroupsGenerator:
    """
    - Given a set of teams with members, create a list of
    pairs where each member is from a different team
    - If there is a history generated, ensure that no pair
    generated has met up in the last month
    """

    teams: set[Team]

    def __init__(self):
        self.teams = set([])

    def add_team(self, team: Team) -> bool:
        if len(team.members) == 0:
            return False
        self.teams.add(team)
        return True

    def get_member_teams_map(self) -> dict[str, set[str]]:
        member_teams_map = {}
        for team in self.teams:
            for member in team.members:
                if member not in member_teams_map:
                    member_teams_map[member] = set([])
                member_teams_map[member].add(team.name)
        return member_teams_map

    def get_pairs(self) -> set[tuple[TeamMember, TeamMember]]:
        """
        Finds pairs of members that aren't from the same team until there
        are no members left.
        """
        members = self.get_members_from_teams()
        shuffle(list(members))

        pairs: set[tuple[TeamMember, TeamMember]] = set([])
        while len(members) > 0:
            pair_member_one = self.get_member_from_members(members)
            pair_member_two = self.get_member_from_members(members)
            if pair_member_one and pair_member_two:
                pairs.add((pair_member_one, pair_member_two))
            else:
                logger.info(
                    f"Couldn't generate pairs from remaining members: {members}"
                )
        return pairs

    def get_member_from_members(self, members: set[TeamMember]) -> TeamMember | None:
        member = members.pop()
        if member:
            return member

    def get_members_from_teams(self) -> set[TeamMember]:
        members: set[TeamMember] = set([])
        for team in self.teams:
            for member in team.members:
                members.add(member)
        return members
