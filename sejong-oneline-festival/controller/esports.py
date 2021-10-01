from datetime import datetime


def make_team_document(
    team_name: str,
    members: dict
):
    return {'team_name': team_name,
            'members': members}


def make_match_log_document(
    participants: list,
    match_round: int,
    match_teams: list
):
    document = {
        'match_round': match_round,
        'match_teams': [],
        'winner_team_idx': None,
        'status': None,
        'created_at': datetime.now()
    }

    for team in match_teams:
        for idx, value in enumerate(participants):
            if team == value['team_name']:
                document['match_teams'].append({'team_idx': idx, 'team_name': team})
                break

    return document
        