from werkzeug.security import generate_password_hash

def make_user_document(
	new_user: dict, user_id: str, password: str, auth_info: dict
):
    new_user['user_id'] = user_id
    new_user['password'] = generate_password_hash(password)
    new_user['roles'] = ['general']
    new_user['name'] = auth_info['name']
    new_user['major'] = auth_info['major']
    return  new_user
