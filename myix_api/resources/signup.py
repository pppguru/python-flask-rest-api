from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token)
from sqlalchemy import exc
import sys

from ..models.usermodel import UserModel
from ..controller.redminecontroller import RedmineController

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'Username cannot be blank', required = True)
parser.add_argument('password', help = 'Password cannot be blank', required = True)
parser.add_argument('email', help = 'Email cannot be blank', required = True)
parser.add_argument('name', help = 'Name cannot be blank', required = True)
parser.add_argument('surname', help = 'Surename cannot be blank', required = True)


"""
@api {post} api/v1/signup Signup
@apiName Signup
@apiGroup Authentication

@apiHeader {String}		Content-Type	application/json

@apiParam {String}		username		Username of the user
@apiParam {String}		password		Password of the user
@apiParam {String}		email			email of the user
@apiParam {String}		name			Name of the user.
@apiParam {String}		surname		Surname of the user.

@apiSuccess {String}	message			User `username` was created.
@apiSuccess {String}	access_token	User Access Token.
@apiSuccess {String}	refresh_token	User Refresh Token.
"""

class SignUpResource(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User `{}` already exists'. format(data['username'])}

        if UserModel.find_by_email(data['email']):
            return {'message': 'User email `{}` already exists'. format(data['email'])}

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password']),
            email = data['email'],
            name = data['name'],
            surname = data['surname'],
        )

        # Register on Redmine if user email is not existing on Redmine
        if not RedmineController.isEmailAlreadyRegistered(data['email']):
            if not RedmineController.registerRedmineUser(
                data['username'],
                data['email'],
                data['name'],
                data['surname']
            ):
                return {'message': 'Redmine registration Error'}, 500

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])

            return {
                'message': 'User {} was created'.format( data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except exc.IntegrityError as err:
            print("Unexpected error:", err)
            return {'message': 'database error'}, 500
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return {'message': 'Something went wrong'}, 500