USERS = {
    "admin": "admin123",
    "supervisor": "1234"
}


def login(username, password):

    return USERS.get(username) == password