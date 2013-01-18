from webtest import TestApp
import unittest
import json
from c3s.api import main


class TestApiVersionViews(unittest.TestCase):

    def test_api_verison_get(self):
        """
        try to get the messages
        """
        app = TestApp(main({}))
        res = app.get('/api_version', status=200)
        answer = (json.loads(res.body))
        #print(answer)  # {u'API version': u'0.1dev'}
        self.assertTrue('0.1dev' in str(answer))


class TestUserViews(unittest.TestCase):

    def test_users_get_unauthorized(self):
        """
        try to get the list of users without being registerd & authenticated
        expecting this to fail!
        """
        app = TestApp(main({}))
        res = app.get('/users', status=401)

        self.failUnless('401 Unauthorized' in res.body)
        self.assertTrue(
            'text/plain' in res.headers['Content-Type'])
        self.assertTrue(
            "This server could not verify" in str(res.body))

    def test_users_put(self):
        """
        register a username, get an auth token, use it to get list of users
        """
        app = TestApp(main({}))
        _name = 'heinzi'
        _namejson = json.dumps({'name': _name})
        res = app.put('/users', _namejson, status=200)
        # print(res)  # uncomment to see the following output:
        # Content-Type: application/json; charset=UTF-8
        # {"api-version": "0.1dev",
        #  "token": "heinz-2354ed39ba5def1aef9f8a11997d8833df691f25"}
        self.assertTrue(
            'application/json; charset=UTF-8' in res.headers['Content-Type'])
        # store the body as json
        #print("the body is json:")
        #print(res.body)
        _json = json.loads(res.body)
        # print(_json['api-version'])
        self.assertTrue('0.1dev' in _json['api-version'])
        self.assertTrue(_name in str(_json['token']))

        _token = _json['token']
        #print("the token from res: " + _token)
        _auth_header = {'X-Messaging-Token': str(_token)}
        # now we have a token and can authenticate...
        res2 = app.get('/users', headers=_auth_header, status=200)

        #print(res2)
        # Response: 200 OK
        # Content-Type: application/json; charset=UTF-8
        # {"users": ["heinz"]}
        self.assertTrue(
            'application/json; charset=UTF-8' in res2.headers['Content-Type'])
        # store the body as json
        _json = json.loads(res2.body)
        #self.assertTrue('0.1dev' in _json['api-version'])
        self.assertTrue(_name in (_json['users']))
        #print(_json.items())

    def test_users_put_same_twice(self):
        """
        try to register the same user twice; must fail!
        """
        app = TestApp(main({}))
        _name = 'john'
        _namejson = json.dumps({'name': _name})
        res = app.put('/users', _namejson)
        # check response
        self.assertTrue("token" in str(res.body))  # did get a token
        self.assertTrue(_name in str(res.body))  # name found
        # do it again, try to register user of same name
        # expect "Bad Request (400)"
        res2 = app.put('/users', _namejson, status=400)
        #print(res2)
# {"status": "error",
#  "errors": [{
#      "location": "url",
#      "name": "name",
#      "description": "This user exists!"}]}
        _json2 = json.loads(res2.body)
        #print(_json2['status'])
        self.assertTrue(
            'error' in _json2['status'])
        self.assertTrue(
            'This user exists!' in _json2['errors'][0]['description'])

    def test_users_delete(self):
        """
        register a username, get an auth token, delete user again
        idea: register second user to check
        """
        app = TestApp(main({}))
        _name = 'mary'
        _namejson = json.dumps({'name': _name})
        res = app.put('/users', _namejson, status=200)
        self.assertTrue(
            'application/json; charset=UTF-8' in res.headers['Content-Type'])
        # store the body as json
        _json = json.loads(res.body)
        #print(_json['token'])
        self.assertTrue('0.1dev' in _json['api-version'])
        self.assertTrue(_name in str(_json['token']))

        _token = _json['token']
        #print("the token from res: " + _token)

        # try using an invalid token: get coverage for the valid_token function
        _invalid_token = _token.replace('-', '')  # removing the '-'
        #print("_invalid_token: " + _invalid_token)
        _auth_header = {'X-Messaging-Token': str(_invalid_token)}
        # calling with the invalid_token we expect 401: Unauthorized
        res2 = app.delete_json('/users', params=_name,
                               headers=_auth_header, status=401)

        _auth_header = {'X-Messaging-Token': str(_token)}
        # now we have a token and can authenticate... and delete the user

        # delete the user
        #res2 = app.delete('/users', params=_name,
        res2 = app.delete_json('/users', params=_name,
                               headers=_auth_header, status=200)
        #print(res2)
        self.assertTrue('goodbye' in json.loads(res2.body).keys())
        self.assertTrue(_name in json.loads(res2.body).values())


class TestMessageViews(unittest.TestCase):

    def test_messages_get(self):
        """
        try to get the messages
        """
        app = TestApp(main({}))
        res = app.get('/', status=200)
        #print(dir(res))
        #print(res)
        messages = (json.loads(res.body))
        self.assertTrue('moo' not in messages)

    def test_messages_post(self):
        """
        try to post a messages
        """
        app = TestApp(main({}))
        res = app.get('/', status=200)

        #print(res)

        _name = 'poster'
        _namejson = json.dumps({'name': _name})
        res = app.put('/users', _namejson, status=200)
#        self.assertTrue(
#            'application/json; charset=UTF-8' in res.headers['Content-Type'])
        # store the body as json
        _json = json.loads(res.body)
        #print(_json['token'])
#        self.assertTrue('0.1dev' in _json['api-version'])
        self.assertTrue(_name in str(_json['token']))

        _token = _json['token']
        #print("the token from res: " + _token)
        _auth_header = {'X-Messaging-Token': str(_token)}
        # now we have a token and can authenticate... and delete the user

        # post a message (not valid JSON)
        _message = "hello world"
        res2 = app.post(
            '/',
            params=(_message),  # not json: coverage f. valid_message()
            headers=_auth_header,
            status=400  # expecting 400: bad request
        )

        # post a message (valid JSON, but not containing 'text')
        _message = {'texte': 'foo'}
        res2 = app.post(
            '/',
            params=json.dumps(_message),
            headers=_auth_header,
            status=400  # expecting 400: bad request
        )
        #print("----result-----")
        #print(res2)
        self.assertTrue("Missing text" in res2)

        # post a message (valid JSON, but of wrong color)
        _message = {'text': 'foo',
                    'color': 'blue'}
        res2 = app.post(
            '/',
            params=json.dumps(_message),
            headers=_auth_header,
            status=400  # expecting 400: bad request
        )
        #print("----result-----")
        #print(res2)
        self.assertTrue("only red and black supported" in res2)

        # post a message with invalid token
        _message = {'text': 'foo'}
        _auth_header_w_invalid_token = {
            'X-Messaging-Token': str(_token + '123')
        }
        res2 = app.post(
            '/',
            params=json.dumps(_message),
            headers=_auth_header_w_invalid_token,
            status=401  # 401: Unauthorized
        )
        self.assertTrue('401 Unauthorized' in res2.body)

        # post a message (valid JSON)
        _message = {'text': 'foo'}
        res2 = app.post(
            '/',
            params=json.dumps(_message),
            headers=_auth_header,
            status=200
        )
        #print("----result-----")
        #print(res2)
        self.assertTrue('status' in json.loads(res2.body).keys())
        self.assertTrue('added' in json.loads(res2.body).values())

        # post one more message
        _message = {'text': 'bar'}
        res3 = app.post(
            '/',
            params=json.dumps(_message),
            headers=_auth_header,
            status=200
        )
        res3

        # get the messages
        res4 = app.get('/', status=200)
        #print(res4)
        messages = (json.loads(res4.body))
        #print(messages)
        message_count = 0
        for message in messages:
            message_count += 1
        self.assertTrue(message_count == 2,
                        'created 2 messages but found a different number')
        self.assertTrue('moo' not in str(messages))
        self.assertTrue('foo' in str(messages))
