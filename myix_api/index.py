from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager



app = Flask(__name__)
# app.debug = True # Enable the debug mode
api = Api(app, prefix="/api/v1")


# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myixuser:myixpassword@localhost/myix'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret'
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Token authentication configuration
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


from .resources.login import LoginResource
from .resources.signup import SignUpResource
from .resources.users import AllUsers, User
from .resources.redmineusers import RedmineUsers, RedmineProjects, RedmineRoles, RedmineAllIssuesList, RedmineUserIssuesList, RedmineIssue, RedmineCreateIssue
from .resources.token import TokenRefresh, UserLogoutAccess, UserLogoutRefresh
from .models.tokenmodel import RevokedTokenModel

# Set the route for the API endpoints
api.add_resource(LoginResource, '/login')
api.add_resource(SignUpResource, '/signup')
api.add_resource(TokenRefresh, '/refreshtoken')
api.add_resource(UserLogoutAccess, '/logout')
api.add_resource(UserLogoutRefresh, '/loginoutrefresh')

api.add_resource(AllUsers, '/users')
api.add_resource(User, '/user/<string:username>', endpoint="user")

api.add_resource(RedmineUsers, '/redmine-users')
api.add_resource(RedmineProjects, '/redmine-projects')
api.add_resource(RedmineRoles, '/redmine-roles')
api.add_resource(RedmineAllIssuesList, '/redmine-all-issues')
api.add_resource(RedmineUserIssuesList, '/redmine-issues')
api.add_resource(RedmineIssue, '/redmine-issue/<string:issue_id>', endpoint="redmineissue")
api.add_resource(RedmineCreateIssue, '/redmine-create-issue')

if __name__ == '__main__':
    app.run(debug=True)
