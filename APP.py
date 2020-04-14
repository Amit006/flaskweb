
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
# from sqlalchemy.engine import default
from werkzeug.datastructures import MultiDict
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
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
app.config['MYSQL_DB'] = 'FlaskDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


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

            flash(u'Successfully SignUP', 'Success')
            # con = mysql.connect()
            # cur = con.cursor()
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO 
                  users (
                      User_id,
                      Uname,
                      Uemail,
                      Upassword
                      )
              VALUES (default ,%s,%s,%s)''', ( username, email, password))
            mysql.connection.commit()
            # return redirect(url_for('Dashboard'))

        else:
            flash(u'All the form fields are required. ', 'Error')

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
            cur = mysql.connection.cursor()
            cur.execute(''' select * from  users where Uemail = %s''',(email))
            results = cur.fetchall()
            print(' ****************** Results ***************')
            print(results)

            # return redirect(url_for('Dashboard'))
        else:
            flash(u'All the form fields are required. ', 'Error')

    return render_template('Signin.html', form=form, results=results)



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