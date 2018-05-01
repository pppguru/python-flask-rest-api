from redminelib import Redmine, exceptions as RedmineException, engines
from flask import jsonify
import sys

from ..config import config

class RedmineController:
    
    # Initliaze the Redmine Object
    redmine = Redmine(config.REDMINE_URL, key=config.REDMINE_ADMIN_API_KEY)

    def issue_to_json(x):
        return {
            'id' : x.id,
            'project_id': x.project.id,
            'project_name': x.project.name,
            'subject': x.subject,
            'description': getattr(x, 'description', ''),
            'tracker_id': x.tracker.id,
            'tracker_name': x.tracker.name,
            'status_id': x.status.id,
            'status_name': x.status.name,
            'priority_id': x.priority.id,
            'priority_name': x.priority.name,
            'category_id': x.category.id if hasattr(x, 'category') else 'null',
            'category_name': x.category.name if hasattr(x, 'category') else 'null',
            'assigned_id': x.assigned_to.id if hasattr(x, 'assigned_to') else 'null',
            'assigned_name': x.assigned_to.name if hasattr(x, 'assigned_to') else 'null',
            'author_id': x.author.id,
            'author_name': x.author.name,
            # 'start_date': x.start_date,
            # 'due_date': x.due_date,
            'done_ratio': x.done_ratio,
            # 'created_on': x.created_on,
            # 'updated_on': x.updated_on,
        }
    
    @classmethod
    def getAllRedmineUsers(cls):
        def to_json(x):
            return {
                'id': x.id,
                'login': x.login,
                'firstname': x.firstname,
                'lastname': x.lastname,
                'mail': x.mail
            }

        return {'redmine_users': list(map(lambda x: to_json(x), cls.redmine.user.all()))}

    @classmethod
    def getAllRedmineProjects(cls):
        def to_json(x):
            return {
                'id': x.id,
                'name': x.name,
                'identifier': x.identifier,
                'description': x.description,
                'homepage': getattr(x, 'homepage', 'null')
            }

        return {'redmine_projects': list(map(lambda x: to_json(x), cls.redmine.project.all()))}

    @classmethod
    def getAllRedmineRoles(cls):
        def to_json(x):
            return {
                'id': x.id,
                'name': x.name
            }

        return {'redmine_roles': list(map(lambda x: to_json(x), cls.redmine.role.all()))}

    @classmethod
    def registerRedmineUser(cls, user_login, email, firstname, lastname):
        user = cls.redmine.user.new();
        user.login = user_login
        user.firstname = firstname
        user.lastname = lastname
        user.mail = email
        # user.auth_source_id = 1;
        # user.must_change_passwd = True;
        user.mail_notification = 'selected';

        try:
            user.save();
            return True;
        except RedmineException.ValidationError as err:
            print("The function (registerRedmineUser) - Redmine Validation Error:", err)
            return False;
        except:
            print("The function (registerRedmineUser) - Unexpected error:")
            return False;

    @classmethod
    def isEmailAlreadyRegistered(cls, email):
        users = cls.redmine.user.filter(name=email); #just use name param to search the duplicate email address
        return True if len(users) > 0 else False;

    @classmethod
    def getRedmineUser(cls, email):
        users = cls.redmine.user.filter(name=email); #just use name param to search the duplicate email address
        return users[0] if len(users) > 0 else None;

    @classmethod
    def getAllIssues(cls):
        issues = cls.redmine.issue.all()
        return {'issues': list(map(lambda x: cls.issue_to_json(x), issues))}

    @classmethod
    def getAllIssuesByAuthor(cls, user_email):
        current_redmine_user = RedmineController.getRedmineUser(user_email);
        if not current_redmine_user:
            return {'message': 'Redmine user {} doesn\'t exist'.format(user_email)}
        
        issues = cls.redmine.issue.filter(author_id=current_redmine_user.id)
        return {'issues': list(map(lambda x: cls.issue_to_json(x), issues))}

    @classmethod
    def createIssue(cls, user_email, data):
        # Get the current redmine user
        current_redmine_user = RedmineController.getRedmineUser(user_email);
        if not current_redmine_user:
            return {'message': 'Redmine user {} doesn\'t exist'.format(user_email)}

        # Get the project
        project = cls.redmine.project.get(data.project_id)
        if not project:
            return {'message': 'Redmine Project {} is not existing'.format(data.project_id)}
        
        # Get the membership of current user
        memberships = project.memberships;
        current_user_membership = list(filter(lambda x: x.user.id == current_redmine_user.id, memberships))

        # Check if the proper role is there (TO-DO : Manually set Manager Role ID - 3)
        PROPER_ROLE_ID = 10; 

        if len(current_user_membership) == 0: # If no membership, then just create it!
            membership = cls.redmine.project_membership.new()
            membership.project_id = data.project_id
            membership.user_id = current_redmine_user.id
            membership.role_ids = [PROPER_ROLE_ID]
            membership.save()
        else:                                 # If existing membership, then just update it!
            membership_id = current_user_membership[0].id
            cls.redmine.project_membership.update(membership_id, role_ids=[PROPER_ROLE_ID])

        # Create the session in behalf of the user, not admin
        with cls.redmine.session(impersonate=current_redmine_user.login):
            issue = cls.redmine.issue.new();
            issue.project_id = data.project_id;
            issue.subject = data.subject;
            issue.description = data.description or "";
            # issue.custom_fields = data.custom_fields or [];

            try:
                issue.save();
                return {'message': 'Redmine Issue {} Created'.format(issue.id)}
            except RedmineException.ValidationError as err:
                print("The function (createIssue) - Redmine Validation Error:", err)
                return {'message': 'Redmine Validation Error'}
            except RedmineException.ForbiddenError as err:
                print("The function (createIssue) - Redmine ForbiddenError Error:", err)
                return {'message': 'Redmine ForbiddenError Error'}
            except:
                print("The function (createIssue) - Unexpected error")
                return {'message': 'Something went wrong'}
    
    @classmethod
    def updateIssue(cls, issue_id, data):
        issue = cls.redmine.issue.get(issue_id);
        if not issue:
            return {'message': 'Redmine issue {} doesn\'t exist'.format(issue_id)}

        if hasattr(data, 'project_id') and data.project_id is not None: 
            issue.project_id = data.project_id;
        if hasattr(data, 'subject') and data.subject is not None: 
            issue.subject = data.subject;
        if hasattr(data, 'description') and data.description is not None: 
            issue.description = data.description;
        if hasattr(data, 'assigned_to_id') and data.assigned_to_id is not None: 
            issue.assigned_to_id = data.assigned_to_id;
        if hasattr(data, 'custom_fields') and data.custom_fields is not None: 
            issue.custom_fields = data.custom_fields;

        try:
            issue.save();
            return {'message': 'Redmine Issue {} Updated'.format(issue_id)}
        except RedmineException.ValidationError as err:
            print("The function (updateIssue) - Redmine Validation Error:", err)
            return {'message': 'Redmine Validation Error'}
        except:
            print("The function (updateIssue) - Unexpected error:", sys.exc_info()[0])
            return {'message': 'Something went wrong'}

    @classmethod
    def getDetailsOfIssue(cls, issue_id):
        issue = cls.redmine.issue.get(issue_id, include='journals,attachments');
        return {
            'project_id': issue.project.id,
            'project_name': issue.project.name,
            'subject': issue.subject,
            'description': issue.description,
            'tracker_id': issue.tracker.id,
            'tracker_name': issue.tracker.name,
            'status_id': issue.status.id,
            'status_name': issue.status.name,
            'priority_id': issue.priority.id,
            'priority_id': issue.priority.name,
            'category_id': issue.category.id if hasattr(issue, 'category') else 'null',
            'category_name': issue.category.name if hasattr(issue, 'category') else 'null',
            'assigned_id': issue.assigned_to.id if hasattr(issue, 'assigned_to') else 'null',
            'assigned_name': issue.assigned_to.name if hasattr(issue, 'assigned_to') else 'null',
            'author_id': issue.author.id,
            'author_name': issue.author.name,
            'done_ratio': issue.done_ratio,
        }

    @classmethod
    def deleteIssue(cls, issue_id):       
        try:
            cls.redmine.issue.delete(issue_id)
            return {'message': 'Redmine Issue {} Deleted'.format(issue_id)}
        except RedmineException.ResourceNotFoundError as err:
            print("The function (deleteIssue) - Redmine ResourceNotFoundError Error:", err)
            return {'message': 'Redmine Issue {} is Not Found'.format(issue_id)}
        except:
            print("The function (deleteIssue) - Unexpected error:", sys.exc_info()[0])
            return {'message': 'Something went wrong'}
