#!/usr/bin/env python3

from flask import request
from flask_restful import Resource
from config import app, db, api, request, session, Resource, make_response
from models import *


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


class ToDoLists(Resource):
    def get(self):

        tdlists = ToDoList.query.all()
        lists_dict = [list.to_dict(only=("id", "description", "created_at",
                                   "users.name", "users.email", "users.id", "items")) for list in tdlists]
        return lists_dict, 200

    def post(Resource):
        data = request.get_json()
        list_description = data.get('description')
        new_list = ToDoList(description=list_description)

        if new_list.validation_errors:
            errors = new_list.validation_errors
            new_list.clear_validation_errors()
            raise Exception(errors)
        try:

            db.session.add(new_list)
            db.session.commit()
            list_dict = new_list.to_dict(
                only=("id", "description", "created_at", "users.name", "users.email", "items"))
            return list_dict, 201
        except:
            errors = new_list.validation_errors
            new_list.clear_validation_errors()
            return {"errors": errors}, 422


class ToDoLists_By_Id(Resource):
    def get(self, id):
        tdl = ToDo.query.filter(ToDo.list_id == id).all() or ToDoList

        if tdl:
            td_dict = [todo.to_dict(
                only=("id", "description", "completed", "todo_list")) for todo in tdl]
            return td_dict, 200
        else:
            return {"error": "List not found."}, 404

    def patch(self, id):
        list = ToDoList.query.filter(ToDoList.id == id).first()
        if list:
            try:
                data = request.get_json()
                for attr in data:
                    setattr(list, attr, data[attr])
                if list.validation_errors:
                    errors = list.validation_errors
                    list.clear_validation_errors()
                    raise Exception(errors)
                db.session.add(list)
                db.session.commit()
                list_dict = list.to_dict()
                return list_dict, 202
            except:
                errors = list.validation_errors
                list.clear_validation_errors()
                return {"error": errors}, 422
        else:
            return {"error": "List not found."}, 404

    def delete(self, id):
        list = ToDoList.query.filter(ToDoList.id == id).first()
        if list:
            db.session.delete(list)
            db.session.commit()
            return {}, 204
        else:
            return {"error": "List not found"}, 404


class ToDos(Resource):
    def get(self):
        tds = ToDo.query.all()
        td_dict = [td.to_dict() for td in tds]
        return td_dict, 200

    def post(self):
        data = request.get_json()
        new_td = ToDo(description=data["description"],
                      completed=False, list_id=data["list_id"])
        print(f"new td {new_td.completed}")
        if new_td.validation_errors:
            errors = new_td.validation_errors
            new_td.clear_validation_errors()
            raise Exception(errors)
        try:
            db.session.add(new_td)
            db.session.commit()
            todo_dict = new_td.to_dict()
            return todo_dict, 201
        except:
            errors = new_td.validation_errors
            new_td.clear_validation_errors()
            return {"errors": errors}, 422


class ToDos_By_Id(Resource):
    def get(self, id):
        td = ToDo.query.filter(ToDo.id == id).first()
        if td:
            td_dict = td.to_dict()
            return td_dict, 200
        else:
            return {"error": " not found."}, 404

    def patch(self, id):
        td = ToDo.query.filter(ToDo.id == id).first()
        if td:
            try:
                data = request.get_json()
                for attr in data:
                    setattr(td, attr, data[attr])
                if td.validation_errors:
                    errors = td.validation_errors
                    td.clear_validation_errors()
                    raise Exception(errors)
                db.session.add(td)
                db.session.commit()
                td_dict = td.to_dict()
                return td_dict, 202
            except:
                errors = td.validation_errors
                td.clear_validation_errors()
                return {"error": errors}, 422
        else:
            return {"error": " not found."}, 404

    def delete(self, id):
        td = ToDo.query.filter(ToDo.id == id).first()
        if td:
            db.session.delete(td)
            db.session.commit()
            return {}, 204
        else:
            return {"error": "ToDo item not found"}, 404


class EditListOwner (Resource):
    def post(self):
        data = request.get_json()
        # owner = User(id=data.get('user_id'))
        # list = ToDoList(id=data.get('list_id'))
        list_id = data.get('list_id')
        user_id = data.get('user_id')
        owner = User.query.filter(User.id == user_id).first()
        list = ToDoList.query.filter(ToDoList.id == list_id).first()
        list_owner = owner in list.users

        try:

            if list_owner:
                list.users.remove(owner)

                db.session.commit()
                updatedList_dict = list.to_dict(only=(
                    "id", "description", "created_at", "users.name", "users.email", "users.id", "items"))
                return updatedList_dict, 200
            else:
                list.users.append(owner)

                db.session.commit()
                updatedList_dict = list.to_dict(only=(
                    "id", "description", "created_at", "users.name", "users.email", "users.id", "items"))
                return updatedList_dict, 200

        except Exception as e:
            print(e)
            return make_response({"errors": e}, 400)


api.add_resource(EditListOwner, '/edit_list_owner')
api.add_resource(ToDoLists, "/todolists")
api.add_resource(ToDoLists_By_Id, "/todolists/<int:id>")
api.add_resource(ToDos, "/todos")
api.add_resource(ToDos_By_Id, "/todos/<int:id>")


if __name__ == '__main__':
    app.run(port=5555, debug=True)
