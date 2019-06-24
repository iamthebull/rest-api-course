from classlib.users import User


def authenticate(username, password):
    user = User.get_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    print(payload)
    user_id = payload['identity']
    return User.get_by_id(user_id)
