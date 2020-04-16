import re

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
# from sqlalchemy.engine import default
from werkzeug.datastructures import MultiDict
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash


app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['SESSION_TYPE'] = 'redis'

bootstrap = Bootstrap(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:N#123456@server/FalskDb'
#db = SQLAlchemy(app)



app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'N#123456'
app.config['MYSQL_DB'] = 'FalskDb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
bcrypt = Bcrypt(app)


# MODEL PORTION
class SignUpFrom(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=35)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('repassword', message='Passwords must match')
    ])
    repassword = PasswordField('repassword')

class SignInForm(Form):
    email = EmailField('email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('password', [validators.DataRequired()])
    rememberMe = BooleanField('rememberMe')




@app.route('/')
def index():
    form = SignUpFrom(request.form)

    return render_template('index.html', name='Amit Nayek')

@app.route('/Signup', methods=['GET', 'POST'])
def SignUp():
    form = SignUpFrom(request.form)

    if request.method == 'POST':
        username = request.form['username'] if request.form['username'] else ''
        email = request.form['email'] if request.form['email'] else ''
        password = request.form['password'] if request.form['password'] else ''
        confirm = request.form['repassword'] if request.form['repassword'] else ''
        print(' username: ', username, ' password: ', password, ' email: ', email, ' confirm: ', confirm)

        print(' validation status: ', form.validate())
        print(' validation errors: ', form.errors)


        if form.validate():

            pw_hash =  generate_password_hash(password).decode('utf-8')
            # con = mysql.connect()
            # cur = con.cursor()
            cur = mysql.connection.cursor()
            cur.execute(''' select * from users where Email=%s''', [email])
            result = results = cur.fetchall()
            print(' result: ', result, 'pw_hash:', pw_hash)
            if(len(result) < 1):
                cur.execute('''INSERT INTO 
                      users (
                          User_id,
                          Uname,
                          Email,
                          UPassword
                          )
                  VALUES (default ,%s,%s,%s)''', ( username, email, pw_hash))
                mysql.connection.commit()
                flash(u'SignUP process Successfully.  ', 'Success')
            else:
                flash(u'You are a register user Please LogIn. ', 'Error')

        # return redirect(url_for('Dashboard'))

        else:
            errString = str(form.errors)
            errString = re.sub(r'{*}*\[*\]*', '', errString)

            flash(errString, 'Error')

    return render_template('Signup.html',)



@app.route('/SignIn', methods=['GET', 'POST'])
def SignIn():
    results = ()
    form = SignInForm(request.form)

    if (session.get('isLogIn')):
        return redirect('Dashboard')


    if request.method == 'POST':
        password = request.form['password'] if request.form['password'] else ''
        email = request.form['email'] if request.form['email'] else ''
        rememberMe = True if 'rememberMe' in request.form else False

        if form.validate():
            cur = mysql.connection.cursor()
            cur.execute(''' select * from  users where Email = %s''',[email])
            results = cur.fetchall()
            print(' ****************** Results ***************')
            print(results)
            if(len(results)):
                if(check_password_hash(results[0]['UPassword'], password)):
                    flash(u'Successfully SignIn', 'Success')
                    session['users'] = results[0]
                    session['isLogIn'] = True
                    return redirect('Dashboard')
                else:
                    flash(u'Please Provide a Correct Password', 'Error')
            else:
                flash(u'You are not a Register User', 'Error')
            # return redirect(url_for('Dashboard'))
        else:
            errString = str(form.errors)
            errString = re.sub(r'{*}*\[*\]*', '', errString)
            flash(errString, 'Error')

    return render_template('Signin.html', form=form, results=results)


@app.route('/Dashboard')
def Dashboard():
    print( ' sessionkey: ', session.get('isLogIn'))
    if(session.get('isLogIn')):
        # return render_template('user/partials/Dashboard.html', userData=session.get('users'))
        return render_template('user/index.html', userData=session.get('users'),brandcamp='DAshboard', dynamic=True, pageName='Dashboard.html')
    else:
        return redirect('SignIn')


@app.route('/Logout', methods=['GET'])
def logout():
    print(' from logout ')
    session.clear()
    return redirect('SignIn')

@app.route('/ForgetPassword')
def ForgotPassword():
    return render_template('ForgetPassword.html',)


@app.route('/getData')
def getData():
    cur = mysql.connection.cursor()
    cur.execute(''' select * from test''')
    results = cur.fetchall()
    print(results)
    return 'Done'


@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'

@app.route('/checkPassword/')
def check():
    password = '$2b$12$Pyq.f.irueih85MvgoW1Zey7c4oQbZJJnFzTYx8f/rWhKfebyuqya'
    # result  = check_password_hash('password', password)
    result = ''
    resultPass = generate_password_hash('password').decode('utf-8')
    print(' resultPass: ', resultPass, ' after encoding: ', resultPass)
    result = check_password_hash(resultPass, 'password')
    print(' result: ', result, ' resultPass: ', resultPass)
    return 'ok'

@app.route('/get/')
def get():
    return session.get('key', 'not set')


if __name__ == '__main__':
    sess = Session()
    sess.init_app(app)
    app.run(debug=True)

#
# @app.route('/add_user' ,methods=['POST'])
# def add_user():
#     UName=request.form.get('uname')
#     UEmail=request.form.get('uemail')
#     UPassword=request.form.get('upassword')
#     cur = mysql.connection.cursor()
#     cur.execute("""INSERT INTO users VALUES (DEFAULT, %s,%s,%s)""",(UName ,UEmail ,UPassword))
#
























































