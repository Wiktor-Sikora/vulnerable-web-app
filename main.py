import sqlite3, os, hashlib
from flask import Flask, jsonify, render_template, request, g, redirect

app = Flask(__name__)
app.database = "database.db"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', data={'status': None, 'query': None})
    elif request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        g.db = connect_db()
        cur = g.db.execute(f"SELECT * FROM employees WHERE username = '{login}' AND password = '{password}'")
        if cur.fetchone():
            return render_template(
                'login.html', 
                data={
                    'status': 'success',
                    'query': f"SELECT * FROM employees WHERE username = '{login}' AND password = '{password}'"
            })
        else:
            return render_template('login.html', 
            data={
                'status': 'fail',
                'query': f"SELECT * FROM employees WHERE username = '{login}' AND password = '{password}'"
            })
        g.db.close()

def connect_db():
    return sqlite3.connect(app.database)

def hash_pass(passw):
	m = hashlib.md5()
	m.update(passw.encode('utf-8'))
	return m.hexdigest()

if __name__ == "__main__":
    if not os.path.exists(app.database):
        with sqlite3.connect(app.database) as connection:
            c = connection.cursor()
            c.execute("""CREATE TABLE employees(username TEXT, password TEXT)""")
            c.execute('INSERT INTO employees VALUES("jerzy", "bardzo_słaby")')
            c.execute('INSERT INTO employees VALUES("User", "15i5j8m3OB!S")')
            c.execute('INSERT INTO employees VALUES("Antenogłowy", "aw2haw123dm_")')
            c.execute('INSERT INTO employees VALUES("Dresonogi", "aiwdj21312adz")')
            c.execute('INSERT INTO employees VALUES("Potężny zakolnik", "n3198awnd2391awj")')
            connection.commit()
            connection.close()

    app.run(host='192.168.8.140', port=4000) # runs on machine ip address to make it visible on netowrk
