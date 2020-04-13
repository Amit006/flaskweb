
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.datastructures import MultiDict
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField

from flask_bootstrap import Bootstrap
# from flask_sqlalchemy import SQLAlchemy
from flask_session import Session


app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['SESSION_TYPE'] = 'redis'

bootstrap = Bootstrap(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:N#123456@server/FlaskDB'
# db = SQLAlchemy(app)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'N#123456'
app.config['MYSQL_DB'] = 'FalskDb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


  # MODEL PORTION
class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class SignInForm(Form):
    email = EmailField('email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('password', [validators.DataRequired()])
    rememberMe = BooleanField('rememberMe')



@app.route('/')
def index():
    return render_template('index.html', name='Amit Nayek')

@app.route('/Signup')
def SignUp():
    return render_template('Signup.html',)

@app.route('/SignIn', methods=['GET', 'POST'])
def SignIn():
    form = SignInForm(request.form)
    print("********************  from ********************")
    print(request.form)
    print('form: ', form)
    print("********************  End *********************")

    if request.method == 'POST':
        password = request.form['password'] if request.form['password'] else ''
        email = request.form['email'] if request.form['email'] else ''
        rememberMe = True if 'rememberMe' in request.form else False


        print(' validation status: ', form.validate())
        print(' validation errors: ', form.errors)

        if form.validate():

            # user = User(form.username.data, form.email.data,
            #             form.password.data)
            # db_session.add(user)

            flash(u'Successfully SignIn', 'Success')
            # return redirect(url_for('Dashboard'))
        else:
            flash(u'All the form fields are required. ', 'Error')

    return render_template('Signin.html', form=form)



@app.route('/Dashboard')
def Dashboard():
    return render_template('Dashboard.html',)


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

@app.route('/get/')
def get():
    return session.get('key', 'not set')


if __name__ == '__main__':
    sess = Session()
    sess.init_app(app)
    app.run(debug=True)