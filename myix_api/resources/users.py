from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from ..models.usermodel import UserModel

userparser = reqparse.RequestParser()
userparser.add_argument('username', help = '', required = False)
userparser.add_argument('password', help = '', required = False)
userparser.add_argument('email', help = '', required = False)
userparser.add_argument('name', help = '', required = False)
userparser.add_argument('surname', help = '', required = False)

"""
@api {get} api/v1/users Get All
@apiName Get All
@apiGroup Users

@apiHeader {String}     Content-Type    application/json.
@apiHeader {String}     Authorization   Authentication Token.

@apiSuccess {Object[]}  users           List of user profiles.
@apiSuccess {String}    users.username  Username of the user.
@apiSuccess {String}    users.password  Password of the user.
@apiSuccess {String}    users.email     Email of the user.
@apiSuccess {String}    users.name      Name of the user.
@apiSuccess {String}    users.surname   Surname of the user.
@apiSuccess {Bool}      users.admin     User's admin status.
"""

"""
@api {delete} api/v1/users Delete All
@apiName Delete All
@apiDescription This should be removed from the final version.
@apiGroup Users

@apiHeader {String}     Content-Type    application/json.
@apiHeader {String}     Authorization   Authentication Token.

@apiSuccess {String}    message         <Number> row(s) deleted.
"""

class AllUsers(Resource):
    @jwt_required
    def get(self):
        return UserModel.return_all()

    # This shoud be removed from final version.
    def delete(self):
        return UserModel.delete_all()


"""
@api {get} api/v1/user/{username} Get User
@apiName Get User
@apiGroup User

@apiHeader {String}     Content-Type    application/json.
@apiHeader {String}     Authorization   Authentication Token.

@apiSuccess {String}    username      Username of the user.
@apiSuccess {String}    password      Password of the user.
@apiSuccess {String}    email         Email of the user.
@apiSuccess {String}    name          Name of the user.
@apiSuccess {String}    surname       Surname of the user.
@apiSuccess {Bool}      admin         User's admin status.
"""

"""
@api {put} api/v1/user/{username} Update User
@apiName Update User
@apiGroup User

@apiHeader {String}     Content-Type    application/json.
@apiHeader {String}     Authorization   Authentication Token.

@apiParam {String}    [username]      Username of the user.
@apiParam {String}    [password]      Password of the user.
@apiParam {String}    [email]         Email of the user.
@apiParam {String}    [name]          Name of the user.
@apiParam {String}    [surname]       Surname of the user.

@apiSuccess {String}    message       User {username} Updated.
"""


"""
@api {delete} api/v1/user/{username} Delete User
@apiName Delete User
@apiGroup User

@apiHeader {String}     Content-Type    application/json.
@apiHeader {String}     Authorization   Authentication Token.

@apiSuccess {String}    message         User {username} deleted.
"""

class User(Resource):
    @jwt_required
    def get(self, username):
        return UserModel.return_user(username)

    @jwt_required
    def put(self, username):
        data = userparser.parse_args()
        return UserModel.update_user(data, username)

    @jwt_required
    def delete(self, username):
        return UserModel.delete_user(username)

