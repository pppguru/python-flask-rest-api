from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..controller.redminecontroller import RedmineController
from ..models.usermodel import UserModel

# Setup the Request Parsers
create_issue_parser = reqparse.RequestParser()
create_issue_parser.add_argument('project_id', help = 'The field cannot be blank', required = True)
create_issue_parser.add_argument('subject', help = 'This field cannot be blank', required = True)
create_issue_parser.add_argument('description', required = False)
create_issue_parser.add_argument('custom_fields', required = False)
create_issue_parser.add_argument('status_id', required = False)
create_issue_parser.add_argument('category_id', required = False)
create_issue_parser.add_argument('assigned_to_id', required = False)

update_issue_parser = reqparse.RequestParser()
update_issue_parser.add_argument('project_id', required = False)
update_issue_parser.add_argument('subject', required = False)
update_issue_parser.add_argument('description', required = False)
update_issue_parser.add_argument('custom_fields', required = False)
update_issue_parser.add_argument('status_id', required = False)
update_issue_parser.add_argument('category_id', required = False)
update_issue_parser.add_argument('assigned_to_id', required = False)

"""
@api {get} api/v1/redmine-users Get All Redmine Users
@apiName Get All Users
@apiGroup Redmine

@apiHeader {String}     Content-Type            application/json.
@apiHeader {String}     Authorization           Authentication Token.

@apiSuccess {Object[]}  redmine_users           List of redmine user profiles.
@apiSuccess {Number}    redmine_users.id        Id of the user.
@apiSuccess {String}    redmine_users.login     Login name of the user.
@apiSuccess {String}    redmine_users.firstname First name of the user.
@apiSuccess {String}    redmine_users.lastname  Last name of the user.
@apiSuccess {String}    redmine_users.mail      Email address of the user.
"""
# Return all Redmine users
class RedmineUsers(Resource):
    @jwt_required
    def get(self):
        return RedmineController.getAllRedmineUsers()

"""
@api {get} api/v1/redmine-projects Get All Redmine Projects
@apiName Get All Projects
@apiGroup Redmine

@apiHeader {String}     Content-Type                    application/json.
@apiHeader {String}     Authorization                   Authentication Token.

@apiSuccess {Object[]}  redmine_projects                List of redmine projects.
@apiSuccess {Number}    redmine_projects.id             Id of the project.
@apiSuccess {String}    redmine_projects.name           Name of the project.
@apiSuccess {String}    redmine_projects.identifier     Identifier of the project.
@apiSuccess {String}    redmine_projects.description    Description of the project.
@apiSuccess {String}    redmine_projects.homepage       Home page url of the project.
"""
#return the list of projects
class RedmineProjects(Resource):
    @jwt_required
    def get(self):
        return RedmineController.getAllRedmineProjects()

"""
@api {get} api/v1/redmine-roles Get All Redmine Roles
@apiName Get All Roles
@apiGroup Redmine

@apiHeader {String}     Content-Type                 application/json.
@apiHeader {String}     Authorization                Authentication Token.

@apiSuccess {Object[]}  redmine_roles                List of redmine roles.
@apiSuccess {Number}    redmine_roles.id             Id of the role.
@apiSuccess {String}    redmine_roles.name           Name of the role.
"""
#return the list of projects
class RedmineRoles(Resource):
    @jwt_required
    def get(self):
        return RedmineController.getAllRedmineRoles()

"""
@api {get} api/v1/redmine-all-issues Get All Redmine Issues
@apiName Get All Issues
@apiGroup Redmine

@apiHeader {String}     Content-Type                application/json.
@apiHeader {String}     Authorization               Authentication Token.

@apiSuccess {Object[]}  issues                      List of redmine issues.
@apiSuccess {Number}    issues.id                   Id of the issue.
@apiSuccess {Number}    issues.project_id           Project ID of the issue.
@apiSuccess {String}    issues.project_name         Project name of the issue.
@apiSuccess {String}    issues.subject              Subject of the issue.
@apiSuccess {String}    issues.description          Description of the issue.
@apiSuccess {Number}    issues.tracker_id           Tracker ID of the issue.
@apiSuccess {String}    issues.tracker_name         Tracker name of the issue.
@apiSuccess {Number}    issues.status_id            Status ID of the issue.
@apiSuccess {String}    issues.status_name          Status name of the issue.
@apiSuccess {Number}    issues.priority_id          Priority ID of the issue.
@apiSuccess {String}    issues.priority_name        Priority name of the issue.
@apiSuccess {Number}    issues.category_id          Category ID of the issue.
@apiSuccess {String}    issues.category_name        Category name of the issue.
@apiSuccess {Number}    issues.assigned_id          Assignee user ID of the issue.
@apiSuccess {String}    issues.assigned_name        Assignee user name of the issue.
@apiSuccess {Number}    issues.author_id            Author user ID of the issue.
@apiSuccess {String}    issues.author_name          Author user name of the issue.
@apiSuccess {Number}    issues.done_ratio           Completeness ratio of the issue.
"""
# Return the list of all issues
class RedmineAllIssuesList(Resource):
    @jwt_required
    def get(self):
        return RedmineController.getAllIssues()

"""
@api {get} api/v1/redmine-issues Get the Redmine Issues of the User
@apiName Get the User Issues
@apiGroup Redmine

@apiHeader {String}     Content-Type                application/json.
@apiHeader {String}     Authorization               Authentication Token.

@apiSuccess {Object[]}  issues                      List of redmine issues.
@apiSuccess {Number}    issues.id                   Id of the issue.
@apiSuccess {Number}    issues.project_id           Project ID of the issue.
@apiSuccess {String}    issues.project_name         Project name of the issue.
@apiSuccess {String}    issues.subject              Subject of the issue.
@apiSuccess {String}    issues.description          Description of the issue.
@apiSuccess {Number}    issues.tracker_id           Tracker ID of the issue.
@apiSuccess {String}    issues.tracker_name         Tracker name of the issue.
@apiSuccess {Number}    issues.status_id            Status ID of the issue.
@apiSuccess {String}    issues.status_name          Status name of the issue.
@apiSuccess {Number}    issues.priority_id          Priority ID of the issue.
@apiSuccess {String}    issues.priority_name        Priority name of the issue.
@apiSuccess {Number}    issues.category_id          Category ID of the issue.
@apiSuccess {String}    issues.category_name        Category name of the issue.
@apiSuccess {Number}    issues.assigned_id          Assignee user ID of the issue.
@apiSuccess {String}    issues.assigned_name        Assignee user name of the issue.
@apiSuccess {Number}    issues.author_id            Author user ID of the issue.
@apiSuccess {String}    issues.author_name          Author user name of the issue.
@apiSuccess {Number}    issues.done_ratio           Completeness ratio of the issue.
"""
# Return the list of User's issues 
class RedmineUserIssuesList(Resource):
    @jwt_required
    def get(self):
        current_username = get_jwt_identity();
        current_user = UserModel.find_by_username(current_username);

        return RedmineController.getAllIssuesByAuthor(current_user.email)

"""
@api {post} api/v1/redmine-create-issue Create an Issue
@apiName Create an Issue
@apiGroup Redmine

@apiHeader {String}     Content-Type        application/json.
@apiHeader {String}     Authorization       Authentication Token.

@apiParam {String}      project_id          Project ID of the issue.
@apiParam {String}      subject             Subject of the issue.
@apiParam {String}      [description]       Description of the issue.
@apiParam {String}      [assigned_to_id]    Assignee ID of the issue.
@apiParam {String}      [status_id]         Status ID of the issue.
@apiParam {String}      [category_id]       Category ID of the issue.
@apiParam {String}      [custom_fields]     Custom fields of the issue.

@apiSuccess {String}    message             Redmine Issue {issue_id} Created.
"""

class RedmineCreateIssue(Resource):
    @jwt_required
    def post(self):
        current_username = get_jwt_identity();
        current_user = UserModel.find_by_username(current_username);
        
        data = create_issue_parser.parse_args()
        return RedmineController.createIssue(current_user.email, data)

"""
@api {get} api/v1/redmine-issue/{issue_id} Get Issue
@apiName Get Issue
@apiGroup Redmine

@apiHeader {String}     Content-Type         application/json.
@apiHeader {String}     Authorization        Authentication Token.

@apiSuccess {Number}    project_id           Project ID of the issue.
@apiSuccess {String}    project_name         Project name of the issue.
@apiSuccess {String}    subject              Subject of the issue.
@apiSuccess {String}    description          Description of the issue.
@apiSuccess {Number}    tracker_id           Tracker ID of the issue.
@apiSuccess {String}    tracker_name         Tracker name of the issue.
@apiSuccess {Number}    status_id            Status ID of the issue.
@apiSuccess {String}    status_name          Status name of the issue.
@apiSuccess {Number}    priority_id          Priority ID of the issue.
@apiSuccess {String}    priority_name        Priority name of the issue.
@apiSuccess {Number}    category_id          Category ID of the issue.
@apiSuccess {String}    category_name        Category name of the issue.
@apiSuccess {Number}    assigned_id          Assignee user ID of the issue.
@apiSuccess {String}    assigned_name        Assignee user name of the issue.
@apiSuccess {Number}    author_id            Author user ID of the issue.
@apiSuccess {String}    author_name          Author user name of the issue.
@apiSuccess {Number}    done_ratio           Completeness ratio of the issue.
"""

"""
@api {put} api/v1/redmine-issue/{issue_id} Update Issue
@apiName Update Issue
@apiGroup Redmine

@apiHeader {String}     Content-Type        application/json.
@apiHeader {String}     Authorization       Authentication Token.

@apiParam {String}      [project_id]        Project ID of the issue.
@apiParam {String}      [subject]           Subject of the issue.
@apiParam {String}      [description]       Description of the issue.
@apiParam {String}      [assigned_to_id]    Assignee ID of the issue.
@apiParam {String}      [status_id]         Status ID of the issue.
@apiParam {String}      [category_id]       Category ID of the issue.
@apiParam {String}      [custom_fields]     Custom fields of the issue.

@apiSuccess {String}    message             Redmine Issue {issue_id} Updated.
"""


"""
@api {delete} api/v1/redmine-issue/{issue_id} Delete Issue
@apiName Delete Issue
@apiGroup Redmine

@apiHeader {String}     Content-Type    application/json.
@apiHeader {String}     Authorization   Authentication Token.

@apiSuccess {String}    message         Redmine Issue {issue_id} Deleted.
"""
# Redmine Issue
class RedmineIssue(Resource):
    @jwt_required
    def get(self, issue_id):
        return RedmineController.getDetailsOfIssue(issue_id)

    @jwt_required
    def put(self, issue_id):
        data = update_issue_parser.parse_args()
        return RedmineController.updateIssue(issue_id, data);
        
    @jwt_required
    def delete(self, issue_id):
        return RedmineController.deleteIssue(issue_id);




