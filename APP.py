from os import name
from flask import Flask, url_for, render_template, request, session, redirect
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path="", static_folder="static")
# Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:N#123456@server/FlaskDB'
db = SQLAlchemy(app)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'N#123456'
app.config['MYSQL_DB'] = 'FlaskDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)





@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/hello')
def hello():
    return render_template('hello.html', name=name)

@app.route('/getData')
def getData():
    cur = mysql.connection.cursor()
    cur.execute(''' select * from test''')
    rv = cur.fetchall()
    # conn.commit()
    return str(rv)




if __name__ == '__main__':
    app.run(debug=True)