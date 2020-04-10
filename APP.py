#from os import name
from flask import Flask, render_template
from flask_mysqldb import MySQL
# from flask_sqlalchemy import SQLAlchemy



#app = Flask(__name__, static_url_path="", static_folder="static")
app = Flask(__name__)
# Bootstrap(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:N#123456@server/FlaskDB'
# db = SQLAlchemy(app)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'N#123456'
app.config['MYSQL_DB'] = 'FalskDb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
@app.route('/')
def index():
    return render_template('Signup.html',)

@app.route('/SignIn')
def hello():
    return render_template('Signin.html',)

@app.route('/getData')
def getData():
    cur = mysql.connection.cursor()
    cur.execute(''' select * from test''')
    results = cur.fetchall()
    print(results)
    return 'Done'

if __name__ == '__main__':
    app.run(debug=True)