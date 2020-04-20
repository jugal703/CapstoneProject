from django.contrib.auth import authenticate, login


def credentials_are_valid(request, username, password):
    """
    This function attempts to authenticate the username and password passed to it
    :param request: Django request object that will store the authenticated session
    :param username: (string) Username being authenticated
    :param password: (string) Password being authenticated
    :return: If credentials authenticate successfully: True
             Else: False
             Side effect: The request's SESSION will be populated with the data from a successfully logged in user
    """
    user = authenticate(username=username, password=password)
    if user is None:
        # The credentials failed to authenticate
        return False
    else:
        login(request, user)
        return True
