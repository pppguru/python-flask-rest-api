from flask import Flask, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'myixuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'myixpassword'
app.config['MYSQL_DATABASE_DB'] = 'myix'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


"""
@api {get} / Request Hello World data
@apiName Hello "space object"
@apiGroup Basic

@apiSuccess {String}	hello			"hello".
@apiSuccess {String}	spaceObject		Name of the space object.
"""
@app.route('/')
def get():
    cur = mysql.connect().cursor()
    cur.execute('''SELECT * FROM test_table''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'myHelloCollection' : r})


"""
@api {get} /users Request All User Data of all users
@apiName Users
@apiGroup Basic

@apiSuccess {Number}	id			User ID.
@apiSuccess {Bool}		admin		User admin status.
@apiSuccess {String}	username	Username of the user.
@apiSuccess {String}	name		Name of the user.
@apiSuccess {String}	surname		Surname of the user.
@apiSuccess {String}	email		E-mail of the user.
@apiSuccess {String}	password	Hash of the user.
"""
@app.route('/users')
def getUsers():
    cur = mysql.connect().cursor()
    cur.execute('''SELECT * FROM users''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'myUsersCollection' : r})

if __name__ == '__main__':
    app.run()

