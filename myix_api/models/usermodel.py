from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import exc

from ..index import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(60), unique = True, nullable = False)
    name = db.Column(db.String(120), unique = False, nullable = True)
    surname = db.Column(db.String(120), unique = False, nullable = True)
    admin = db.Column(db.Boolean(), unique = False, nullable = True );

    def save_to_db(self):
        print("self:", self)
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password,
                'email': x.email,
                'name': x.name,
                'surname': x.surname,
                'admin': x.admin,
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}


    @classmethod
    def return_user(cls, username):
        current_user = UserModel.find_by_username(username)
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(username)}
        return {'username': current_user.username,
                'password': current_user.password,
                'email': current_user.email,
                'name': current_user.name,
                'surname': current_user.surname,
                'admin': current_user.admin,
                }

    @classmethod
    def update_user(cls, data, username):
        current_user = UserModel.find_by_username(username)
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(username)}

        if data.password:
            current_user.password = UserModel.generate_hash(data.password)

        current_user.username = data.username or current_user.username
        current_user.email = data.email or current_user.email
        current_user.name = data.name or current_user.name
        current_user.surname = data.surname or current_user.surname
        db.session.commit()

        return {'message': 'User {} Updated'.format(username)}


    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except exc.IntegrityError as err:
            print("Database error:", err)
            return {'message': 'database error'}
        except:
            return {'message': 'Something went wrong'}


    @classmethod
    def delete_user(cls, username):
        current_user = UserModel.find_by_username(username)
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(username)}
        try:
            db.session.delete(current_user)
            db.session.commit()
            return {'message': 'User {} Deleted'.format(current_user.username)}
        except exc.IntegrityError as err:
            print("Database error:", err)
            return {'message': 'database error'}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)