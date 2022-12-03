import base64
import datetime
import hashlib
import random
import re
import sqlite3
import zlib

from flask import Flask, render_template, request, make_response, redirect
from secret import PASSWORD_SALT, TOKEN_SECRET

conn = sqlite3.connect('/tmp/app.db', check_same_thread=False)
conn.load_extension('/app/lib/token_ext.so')
cursor = conn.execute("select token_ext_init(x'{}')".format(TOKEN_SECRET))
assert (cursor.fetchone()[0] == 0)

conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    userid INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# from https://raw.githubusercontent.com/reggi/fortune-cookie/master/fortune-cookies.txt
with open('/app/resources/fortunes.txt') as f:
    fortunes = list(map(lambda x: x.strip(), f.readlines()))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    token = request.cookies.get('token')
    if token:
        cursor = conn.execute('SELECT token_decrypt(x\'{}\')'.format(base64.b64decode(token.encode()).hex()))
        result = cursor.fetchone()
        try:
            userid, username, password = result[0].decode().split('|')

            cursor = conn.execute(
                'SELECT * FROM users WHERE userid = ? AND username = ? AND password = ?',
                [userid, username, password]
            )
            result = cursor.fetchall()
            assert len(result) != 0
        except:
            response = make_response('Invalid token', 401)
            response.delete_cookie('token')
            return response

        random.seed(zlib.crc32((token + datetime.datetime.now().strftime('%Y%m%d')).encode()))
        fortune = random.choice(fortunes)

        response = make_response(render_template('index.html', username=username, fortune=fortune), 200)
        return response
    else:
        response = make_response(render_template('index.html'), 200)
        return response 

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        response = make_response(render_template('signin.html'), 200)
        return response
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor = conn.execute(
            'SELECT token_encrypt(userid || "|" || username || "|" || password) FROM users WHERE username = ? AND password = ?',
            [username, hashlib.sha256(PASSWORD_SALT + password.encode()).hexdigest()]
        )
        result = cursor.fetchall()
        if len(result) == 0:
            response = make_response('Login failed', 401)
            return response
        
        response = make_response(redirect('/'), 302)
        response.set_cookie('token', base64.b64encode(result[0][0]).decode())
        return response    
        
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        response = make_response(render_template('signup.html'), 200)
        return response
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if \
            not ((type(username) is str) and (type(password) is str)) or \
            not ((len(username) >= 8) and (len(password) >= 8)) or \
            not re.match(r'^[a-zA-Z0-9]+$', username):
            response = make_response('Bad username or password', 400)
            return response

        cursor = conn.execute('SELECT userid FROM users WHERE username = ?', [username])
        result = cursor.fetchall()
        if len(result) != 0:
            response = make_response('Duplicate username', 400)
            return response

        conn.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            [username, hashlib.sha256(PASSWORD_SALT + password.encode()).hexdigest()]
        )
        conn.commit()

        response = make_response(redirect('/'), 302)
        return response

@app.route('/signout', methods=['GET'])
def signout():
    response = make_response(redirect('/'), 302)
    response.delete_cookie('token')
    return response
