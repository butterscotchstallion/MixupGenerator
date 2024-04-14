"""
- Given a set of teams with members, create a list of
pairs where each member is from a different team
- If there is a history generated, ensure that no pair
generated has met up in the last month
"""

from mixup_generator.mixup_generator import MixupGenerator
from mixup_generator.mixup_team import MixupTeam
from mixup_generator.mixup_team_member import MixupTeamMember


def test_add_team():
    generator = MixupGenerator()
    member_names: set[MixupTeamMember] = set(
        [
            MixupTeamMember(name="Professor Farnsworth"),
            MixupTeamMember(name="Toranga Leela"),
            MixupTeamMember(name="Fry"),
            MixupTeamMember(name="Zoidberg"),
        ]
    )

    team = MixupTeam(name="Alpha", members=member_names)
    team_added = generator.add_team(team)

    assert team_added, "Team has no members"

    # Adding same team intentionally to test duplicates
    generator.add_team(team)

    assert len(generator.teams) == 1, "Failed to add team"


def test_get_pairs_from_teams():
    """
    1. Create teams
    2. Find pairs that are from separate teams until there are no
    members without a pair
    3. Figure out what to do with odd numbers (one person has to meet up twice)
    """
    generator = MixupGenerator()
    generator.add_team(
        MixupTeam(
            name="Bravo",
            members=set(
                [
                    MixupTeamMember(name="Professor Farnsworth"),
                    MixupTeamMember(name="Turanga Leela"),
                    MixupTeamMember(name="Philip J. Fry"),
                    MixupTeamMember(name="Doctor Zoidberg"),
                ]
            ),
        )
    )
    generator.add_team(
        MixupTeam(
            name="Charlie",
            members=set(
                [
                    MixupTeamMember(name="Lrrr"),
                    MixupTeamMember(name="Bender Bending Rodriguez"),
                    MixupTeamMember(name="Amy Wong"),
                    MixupTeamMember(name="Hermes Conrad"),
                ]
            ),
        )
    )

    assert len(generator.teams) == 2

    """
    1. Get pairs
    2. Build map of members to their teams
    3. Ensure members that are on more than one team are
    accommodated
    4. Verify each pair has members of separate teams
    """
    all_team_members = generator.get_members_from_teams()
    assert len(all_team_members) > 0

    # Verify member -> team mapping
    member_teams_map = generator.get_member_teams_map()
    for member in member_teams_map:
        assert len(member_teams_map[member]) >= 1

    pairs = generator.get_pairs()

    assert pairs and len(pairs) == 4

    for pair in pairs:
        assert pair[0] in member_teams_map, f"{pair[0]} is not in the map"
        assert pair[1] in member_teams_map, f"{pair[1]} is not in the map"

        first_pair_teams = member_teams_map[pair[0]]
        second_pair_teams = member_teams_map[pair[1]]
        assert pair[0] not in second_pair_teams, "Member one is on member two's team!"
        assert pair[1] not in first_pair_teams, "Member two is on member one's team!"

    print(pairs)


def test_generate_default_username():
    member_name_username_map = {
        "Jenny McNeal": "jmcneal",
        "Scruffy Scruffington": "sscruffington",
        "Fishy Joe Gilman": "fgilman",
        "Leo Wong": "lwong",
        "Linda van Schoonhoven": "lschoonhoven",
    }
    members = [
        MixupTeamMember(name="Jenny McNeal"),
        MixupTeamMember(name="Scruffy Scruffington"),
        MixupTeamMember(name="Fishy Joe Gilman"),
        MixupTeamMember(name="Leo Wong"),
        MixupTeamMember(name="Linda van Schoonhoven", username="custom_username"),
    ]

    for member in members:
        # Test custom username
        if member.name == "Linda van Schoonhoven":
            assert member.username == "custom_username"
        else:
            assert (
                member.username == member_name_username_map[member.name]
            ), "Invalid username"
