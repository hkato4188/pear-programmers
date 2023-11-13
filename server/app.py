#!/usr/bin/env python3

from flask import request
from flask_restful import Resource


from config import app, db, api, request, session, Resource, make_response
from models import User


@app.route('/')
def index():
    return '<h1>Project Server</h1>'


# 1.✅ Create a Signup route
class Signup (Resource):
    # 1.2 The signup route should have a post method
    def post(self):
        # 1.2.1 Get the values from the request body with get_json
        rq = request.get_json()
        User.clear_validation_errors()
        try:
            # 1.2.2 Create a new user, however only pass email/username ( and any other values we may have )
            new_user = User(
                name=rq['name'],
                # 1.2.3 Call the password_hash method on the new user and set it to the password from the request
                email=rq['email'],
                password_hash=rq['password']
            )

            # 1.2.4 Add and commit
            db.session.add(new_user)
            db.session.commit()

            # 1.2.5 Add the user id to session under the key of user_id
            print("the user has been saved!")
            session['user_id'] = new_user.id

            # 1.2.6 send the new user back to the client with a status of 201
            return new_user.to_dict(), 201
        # except Exception as e:
        except:
            return {"error": "{Error signing up}"}, 422

    # 1.3 Test out your route with the client

    # 1.1 Use add_resource to add a new endpoint '/signup'
api.add_resource(Signup, '/signup', endpoint='signup')

# 2.✅ Test this route in the client/src/components/Authentication.sj

# 3.✅ Create a Login route


class Login (Resource):
    def post(self):
        name = request.get_json()['name']
        email = request.get_json()['email']
        password = request.get_json()['password']

        user = User.query.filter(User.name.like(f'{ name }')).first(
        ) or User.query.filter(User.email.like(f'{ email }')).first()

        if user and user.authenticate(password):

            session['user_id'] = user.id

            session.modified = True
            print(session)
            print("hk and Phillip test:")
            print(session['user_id'])
            response = user.to_dict(only=("id", "name", "email")), 200

            return response

        else:
            return {'errors': ['Invalid username or password.']}, 401


api.add_resource(Login, '/login', endpoint='login')


# 4.✅ Create an AutoLogin class that inherits from Resource
# 4.1 use api.add_resource to add an automatic login route
# 4.2 Create a get method
# 4.2.1 Access the user_id from session with session.get
# 4.2.2 Use the user id to query the user with a .filter
# 4.2.3 If the user id is in sessions and found make a response to send to the client. else raise the Unauthorized exception
class AutoLogin (Resource):
    def get(self):

        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            if user:
                return user.to_dict(only=("id", "name", "email")), 200
            else:
                return {'errors': ['User not found.']}, 404
        else:
            return {}, 204


api.add_resource(AutoLogin, '/auto_login')
# 5.✅ Head back to client/src/App.js and try refreshing the page and checking if the user stays logged in...

# 6.✅ Logout
# 6.1 Create a class Logout that inherits from Resource
# 6.2 Create a method called delete
# 6.3 Clear the user id in session by setting the key to None
# 6.4 create a 204 no content response to send back to the client


class Logout (Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204


api.add_resource(Logout, '/logout')

# 7.✅ Navigate to client/src/components/Navigation.js to build the logout button!


if __name__ == '__main__':
    app.run(port=5555, debug=True)
