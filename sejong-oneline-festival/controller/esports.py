from flask import g

def make_team_document(
    team_name: str,
    members: dict
):
    return {'team_name': team_name,
            'members': members}
