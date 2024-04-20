from mixup_generator.groups_generator import GroupsGenerator
from mixup_generator.markup_generator import MarkupGenerator
from mixup_generator.team import Team
from mixup_generator.team_member import TeamMember


def test_markup_generator():
    """
    Tests generation of markup for Confluence
    """
    markup_generator = MarkupGenerator()

    groups_generator = GroupsGenerator()
    groups_generator.add_team(
        Team(
            name="Delta",
            members=set(
                [
                    TeamMember(name="Leelabot"),
                    TeamMember(name="Mad Hatter Robot"),
                    TeamMember(name="Antonio Calculon, Jr."),
                ]
            ),
        )
    )
    groups_generator.add_team(
        Team(
            name="Echo",
            members=set(
                [
                    TeamMember(name="Billionairebot"),
                    TeamMember(name="The Clearcutter"),
                    TeamMember(name="Unit 2013"),
                ]
            ),
        )
    )
    pairs = groups_generator.get_pairs()
    pairs_table: dict = markup_generator.get_table_from_pairs(pairs)

    for row in pairs_table["data"]:
        assert len(row[0]) > 0, "Pair member one is blank!"
        assert len(row[1]) > 0, "Pair member two is blank!"

    # Verify table is in expected format
    markup = markup_generator.generate_table_markup(pairs_table)


def verify_table_header(self, header_markup: str, header_data: tuple[str]) -> bool:
    """
    ||heading 1||heading 2||heading 3||
    """
    has_surrounding_columns = header_markup[0] == "|" and header_markup[-1] == "|"

    return has_surrounding_columns
