""" Cornice services.
"""

import os
import json
import binascii
#from webob import Response
from webob.exc import HTTPUnauthorized
#from webob.exc import HTTPError
from cornice import Service


api_ver = '0.1dev'


def _create_token():
    return binascii.b2a_hex(os.urandom(20))


#class _401(HTTPError):
#    def __init__(self, msg='Unauthorized'):
#        body = {'status': 401, 'message': msg}
#        Response.__init__(self, json.dumps(body))
#        self.status = 401
#        self.content_type = 'application/json'


def valid_token(request):
    header = 'X-Messaging-Token'

    token = request.headers.get(header)
    if token is None:
        raise HTTPUnauthorized()

    token = token.split('-')
    if len(token) != 2:
        raise HTTPUnauthorized()

    user, token = token

    valid = user in _USERS and _USERS[user] == token
    if not valid:
        raise HTTPUnauthorized()

    request.validated['user'] = user


def unique(request):
    name = request.body
    if name in _USERS:
        request.errors.add('url', 'name', 'This user exists!')
    else:
        user = {'name': name, 'token': _create_token()}
        request.validated['user'] = user


api_version = Service(
    name='api_version', path='/api_version', description="API version")


@api_version.get()
def get_info(request):
    """Returns API version in JSON."""
    return {'API version': '0.1dev'}


_USERS = {}
_MESSAGES = []

users = Service(name='users', path='/users', description="Users")
messages = Service(name='messages', path='/', description="Messages")


@users.get(validators=valid_token)
def get_users(request):
    """Returns a list of all users."""
    return {'users': _USERS.keys()}


@users.put(validators=unique)
def create_user(request):
    """Adds a new user."""
    user = request.validated['user']
    _USERS[user['name']] = user['token']
    return {
        'api-version': api_ver,
        'token': '%s-%s' % (user['name'], user['token'])}


@users.delete(validators=valid_token)
def del_user(request):
    """Removes the user."""
#    print("--------the request as arrived in del_user--------")
#    print(request)
#    print("--------the request._body__del--------")
#    print(request._body__del())
#    print("--------the request.validated--------")
#    print(request.validated)
    #print(dir(request))
#    print("------the USERS------")
#    print(_USERS)
    user = request.validated['user']
#    print("about to delete " + user)
#    print("dir(_USERS)")
#    print(dir(_USERS))
#    print(type(_USERS))
#    del _USERS[user['name']]
    _USERS.pop(user)
    return {'goodbye': user}


#
# Messages managment
#
def valid_message(request):
    try:
        message = json.loads(request.body)
    except ValueError:
        request.errors.add('body', 'message', 'Not valid JSON')
        return

    # test...
    #print("-----------------------")
    #print(request)
    #print("-----------------------")
    # make sure we have the fields we want
    if 'text' not in message:
        request.errors.add('body', 'text', 'Missing text')
        return

    if 'color' in message and message['color'] not in ('red', 'black'):
        request.errors.add('body', 'color', 'only red and black supported')
    elif 'color' not in message:
        message['color'] = 'black'

    message['user'] = request.validated['user']
    request.validated['message'] = message


@messages.get()
def get_messages(request):
    """Returns the 5 latest messages"""
    return _MESSAGES[:5]


@messages.post(validators=(valid_token, valid_message))
def post_message(request):
    """Adds a message"""
    _MESSAGES.insert(0, request.validated['message'])
    return {'status': 'added'}
