from flask_restful import Resource
from flask_jwt_extended import (create_access_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from sqlalchemy import exc

from ..models.tokenmodel import RevokedTokenModel

"""
@api {post} api/v1/refreshtoken Refresh Token
@apiName Refresh Token
@apiGroup Authentication

@apiHeader {String}		Content-Type	application/json.
@apiHeader {String}		Authorization	Authentication Token.

@apiSuccess {String}	access_token	User Access Token.
"""

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


"""
@api {post} api/v1/logout Logout
@apiName Logout
@apiGroup Authentication

@apiHeader {String}		Content-Type	application/json.
@apiHeader {String}		Authorization	Authentication Token.

@apiSuccess {String}	message			Access token has been revoked.
"""

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except exc.IntegrityError as err:
            print("Unexpected error:", err)
            return {'message': 'database error'}, 500
        except:
            return {'message': 'Something went wrong'}, 500

"""
@api {post} api/v1/logout Logout Refresh
@apiName Logout Refresh
@apiGroup Authentication

@apiHeader {String}		Content-Type	application/json.
@apiHeader {String}		Authorization	Authentication Refresh Token.

@apiSuccess {String}	message			Refresh token has been revoked.
"""
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except exc.IntegrityError as err:
            print("Unexpected error:", err)
            return {'message': 'database error'}, 500
        except:
            return {'message': 'Something went wrong'}, 500