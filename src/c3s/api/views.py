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


# utility function
def _create_token():
    """create some random token"""
    return binascii.b2a_hex(os.urandom(20))


#class _401(HTTPError):
#    def __init__(self, msg='Unauthorized'):
#        body = {'status': 401, 'message': msg}
#        Response.__init__(self, json.dumps(body))
#        self.status = 401
#        self.content_type = 'application/json'


def valid_token(request):
    """

     **valid_token(request)** (validator function):
       - check whether token is valid

    """
    header = 'X-Messaging-Token'

    token = request.headers.get(header)
    if token is None:
        # there was no token in the header: no auth!
        raise HTTPUnauthorized()

    token = token.split('-')
    if len(token) != 2:
        # the token was mal-formed
        raise HTTPUnauthorized()

    user, token = token

    valid = user in _USERS and _USERS[user] == token
    #print("===== debugging _USERS =====")
    #print(_USERS)
    #print("===========================")
    if not valid:
        raise HTTPUnauthorized()

    request.validated['user'] = user


def unique(request):
    """

     **unique(request)** (validator function):
       - check whether username is unique (or already exists)

    """
    name = request.body
    if name in _USERS:
        request.errors.add('url', 'name', 'This user exists!')
    else:
        user = {'name': name, 'token': _create_token()}
        request.validated['user'] = user


# declare a web service at /api_version
api_version = Service(
    name='api_version', path='/api_version',
    description="API version will return the version of the API")


# a GET call: what a browser does when calling a URL
# point your browser at http://API_IP/api_version to test
@api_version.get()
def get_info(request):
    """Returns API version in JSON.

    pointing a browser at http://API_IP/api_version will yield sth like
    ::

      {'API version': '0.1dev'}

    """
    return {'API version': '0.1dev'}

#
# User Management
#
# a dict of users
_USERS = {}
# definition of a service
users = Service(name='users', path='/users', description="User management")


# another GET
@users.get(validators=valid_token)
def get_users(request):
    """Returns a list of all users."""
    return {'users': _USERS.keys()}
# test this one with curl on the command line:
# $ curl http://localhost:6543/users
# {"status": 401, "message": "Unauthorized"}


# PUT
@users.put(validators=unique)
def create_user(request):
    """Adds a new user.

    returns api-version and token for further interaction
    ::

        {
            'api-version': 0.1dev,
            'token': 'exampleuser-a02398f4de23b43a2223'
        }

    """
    user = request.validated['user']
    _USERS[user['name']] = user['token']

    return {
        'api-version': api_ver,
        'token': '%s-%s' % (user['name'], user['token'])}


# DELETE
@users.delete(validators=valid_token)
def del_user(request):
    """
    Removes the user.

    has to be called with token in header.

    returns
    ::
        {'goodbye': exampleusername}

    """
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
# a list of messages
_MESSAGES = []
#
# another service
messages = Service(name='messages', path='/', description="Message management")


def valid_message(request):
    """

     **valid_message(request)** (validator function):
       - utility function to check validity of messages

    """
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


# GET
@messages.get()
def get_messages(request):
    """Returns the 5 latest messages

    returns
    ::

        list of messages

    """
    return _MESSAGES[:5]


# POST
@messages.post(validators=(valid_token, valid_message))
def post_message(request):
    """
    Adds a message

    returns
    ::
        {'status': 'added'}

    """
    _MESSAGES.insert(0, request.validated['message'])
    return {'status': 'added'}
