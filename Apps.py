
from flask import Flask,render_template
#from flask_mysqldb import MySQL




#

# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'N#123456'
# app.config['MYSQL_DB'] = 'FalskDb'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#mysql = MySQL(app)

app = Flask(__name__)
@app.route('/SignIn')
def index():
    return render_template('SignIn.html',)

@app.route('/Signup')
def hello():
    return render_template('Signup.html',)


if __name__ == '__main__' :
    app.run(debug=True)