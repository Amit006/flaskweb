from flask import Flask,render_template,request,flash,redirect

from flask_mysqldb import MySQL
import mysql.connector

from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField

from flask_bootstrap import Bootstrap


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
class SignupForm(Form):
    Name = StringField('Name', [validators.Length(min=4, max=25)])
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
def Signup():
    return render_template('Signup.html',)

@app.route('/SignIn', methods=['GET', 'POST'])
def SignIn():
    form = SignInForm(request.form)
    print("********************  from ********************")
    print(request.form)
    print('form: ', form)
    print("********************  End *********************")
    result = []
    if request.method == 'POST':
        password = request.form['password'] if request.form['password'] else ''
        email = request.form['email'] if request.form['email'] else ''
        rememberMe = True if 'rememberMe' in request.form else False
        print(' password: ', password, ' email: ', email, ' rememberMe: ', rememberMe )



        if form.validate():

            # user = User(form.username.data, form.email.data,
            #             form.password.data)
            # db_session.add(user)

            flash(u'Successfully SignIn', 'Success')
            cur = mysql.connection.cursor()
            sql = '''select * from FalskDb.users where Email=%s'''
            print(sql)
            cur.execute(sql, (email,))
            data = cur.fetchall()
            print(' result: ', data)
            # data.close()
            # return redirect(url_for('Dashboard'))
        else:
            flash(u'All the form fields are required. ', 'Error')

    return render_template('Signin.html', form=form, result=result)

@app.route('/ForgetPassword')
def ForgotPassword():
    return render_template('ForgetPassword.html',)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/getData',methods=['POST'])
def getData():
    email=request.form.get('email')
    password=request.form.get('password')

    cur = mysql.connection.cursor()
    cur.execute(''' SELECT * from users ''')
    results = cur.fetchall()
    if len(results)>0 :
        return redirect('/dashboard')
    else:
        return redirect('/SignIn')


# @app.route('/getData')
# def getData():
#     cur = mysql.connection.cursor()
#     cur.execute(''' select * from users''')
#     results = cur.fetchall()
#     return results


# @app.route('/add_user' ,methods=['POST'])
# def add_user():
#     UName=request.form.get('uname')
#     UEmail=request.form.get('uemail')
#     UPassword=request.form.get('upassword')
#     cur = mysql.connection.cursor()
#     cur.execute("""INSERT INTO users VALUES (DEFAULT, %s,%s,%s)""",(UName ,UEmail ,UPassword))


    # connection = mysql.connect()
    # connection.commit()
    mysql.connection.commit()
    return  "User registered successfully"



if __name__ == '__main__':
    app.run(debug=True)




















