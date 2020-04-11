from flask import Flask,render_template,request
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'N#123456'
app.config['MYSQL_DB'] = 'FalskDb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('SignIn.html')


@app.route('/Signup')
def about():
    return render_template('Signup.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/SignIn_validation', methods=['post'])
def SignIn_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    return " The email is {} and The password is{} ".format(email,password)


if __name__ == "__main__":

 app.run(debug=True)