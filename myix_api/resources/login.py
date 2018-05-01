from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

from ..models.usermodel import UserModel
from ..controller.redminecontroller import RedmineController

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

"""
@api {post} api/v1/login Login
@apiName Login
@apiGroup Authentication

@apiHeader {String}		Content-Type	application/json

@apiParam {String}		username		Username of the user
@apiParam {String}		password		Password of the user

@apiSuccess {String}	message			Logged in as Username.
@apiSuccess {String}	access_token	User Access Token.
@apiSuccess {String}	refresh_token	User Refresh Token.
"""
class LoginResource(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            # Register on Redmine if user email is not existing on Redmine
            if not RedmineController.isEmailAlreadyRegistered(current_user.email):
                if not RedmineController.registerRedmineUser(
                    current_user.username,
                    current_user.email,
                    current_user.name,
                    current_user.surname
                ):
                    return {'message': 'Redmine registration Error'}, 500

            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}
        return data