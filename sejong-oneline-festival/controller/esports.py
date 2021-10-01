from flask import g

def make_team_document(
    team_name: str,
    members: dict
):
    return {'team_name': team_name,
            'members': members}


def make_event_document(event: dict):
    return {
        'event_id': event['_id'],
        'name': event['name'],
        'banner_photo': event['banner_photo'],
        'status': event['status'],
        'created_at': event['created_at']
    }


def make_tournament(match_logs: list):
    document = {
        0: [],
        1: [],
        2: [],
        3: [] 
    }
    for r in range(2):
        for match in match_logs:
            if match['match_round'] == r:
                document[r] += [match['link'], match['match_teams']]
    for match in match_logs:
        if match['match_round'] == 2 and match['winner_team']:
            document[3] += [None, match['winner_team']]
            break
    return document

