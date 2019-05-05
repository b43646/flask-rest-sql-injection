import sqlite3, os, hashlib
from flask import Flask, jsonify, render_template, request, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
app.database = "sample.db"

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

class User(Resource):
    def get(self):
        return jsonify({'status': '200'})

    def post(self):
        args = parser.parse_args()
        print args
    	if request.method == 'POST':
       	    uname,pword = (args['username'],args['password'])
            print uname, pword
            g.db = connect_db()
            cur = g.db.execute("SELECT * FROM employees WHERE username = '%s' AND password = '%s'" %(uname, hash_pass(pword)))
            if cur.fetchone():
                result = {'status': 'success'}
            else:
                result = {'status': 'fail'}
            g.db.close()
            return jsonify(result)


@app.errorhandler(404)
def page_not_found_error(error):
    return render_template('error.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error=error)

def connect_db():
    return sqlite3.connect(app.database)

# Create password hashes
def hash_pass(passw):
	m = hashlib.md5()
	m.update(passw)
	return m.hexdigest()




api.add_resource(User, '/login')

if __name__ == "__main__":

    #create database if it doesn't exist yet
    if not os.path.exists(app.database):
        with sqlite3.connect(app.database) as connection:
            c = connection.cursor()
            c.execute("""CREATE TABLE shop_items(name TEXT, quantitiy TEXT, price TEXT)""")
            c.execute("""CREATE TABLE employees(username TEXT, password TEXT)""")
            c.execute('INSERT INTO shop_items VALUES("water", "40", "100")')
            c.execute('INSERT INTO shop_items VALUES("juice", "40", "110")')
            c.execute('INSERT INTO shop_items VALUES("candy", "100", "10")')
            c.execute('INSERT INTO employees VALUES("itsjasonh", "{}")'.format(hash_pass("badword")))
            c.execute('INSERT INTO employees VALUES("loren", "{}")'.format(hash_pass("12345")))
            c.execute('INSERT INTO employees VALUES("newguy29", "{}")'.format(hash_pass("pass123")))
            connection.commit()
            connection.close()

    app.run(host='0.0.0.0', debug=True) # runs on machine ip address to make it visible on netowrk
