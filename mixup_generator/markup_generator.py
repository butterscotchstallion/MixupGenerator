from mixup_generator.team_member import TeamMember


class MarkupGenerator:
    """
    Generates markup for a Confluence table based on
    supplied pairs of team members
    """

    def generate_table_markup(self, pairs_table_data: dict) -> str:
        """
        Generates header and column markup based on table format.

        1. Create set of strings representing each line of the table,
        starting with the header
        2. Join the lines using newline
        """
        markup_lines: set[str] = set([])

        # Headers
        table_header = pairs_table_data["header"]
        first_header = self.get_header_markup(table_header[0])
        second_header = self.get_header_markup(table_header[1])
        markup_lines.add(f"|{first_header}{second_header}|")

        # Data
        for row in pairs_table_data["data"]:
            markup_lines.add(self.get_column_from_row(row))

        return "\n".join(list(markup_lines))

    def get_column_from_row(self, row: tuple[str]) -> str:
        """
        |cell A1|cell A2|cell A3|
        """
        return f"|{"|".join(row)}|"

    def get_header_markup(self, header_text: str) -> str:
        """
        ||heading 1||heading 2||heading 3||
        """
        return f"|{header_text}|"

    def get_table_from_pairs(
        self, pairs: set[tuple[TeamMember, TeamMember]]
    ) -> dict[str, tuple[str, str] | set[tuple[str, str]]]:
        """
        Formats pairs data into what is used in the table

        In the Python representation, this is represented
        as a set of tuples, and each row is a tuple of strings
        with the usernames of the team members

        Team Member 1    , Team Member 2
        column one       , column two
        pair one username, pair two username
        """
        pairs_table: set[tuple[str, str]] = set([])

        # headings
        header = ("Team Member 1", "Team Member 2")

        for pair in pairs:
            pairs_table.add((pair[0].username, pair[1].username))

        return {"header": header, "data": pairs_table}
