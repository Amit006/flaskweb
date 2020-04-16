from flask import Flask
from flask_mail import Mail,Message
#import smtplib
import socket
socket.getdefaulttimeout()


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] =('smtp.gmail.com')   #smtplib.SMTP('smtp.gmail.com')
app.config['MAIL_PORT'] =  465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] ='shahbazaslam708@gmail.com'
app.config['MAIL_PASSWORD'] = 'Shabby_12' #'$2b$12$Pyq.f.irueih85MvgoW1Zey7c4oQbZJJnFzTYx8f/rWhKfebyuqya'
app.config['MAIL_DEFAULT_SENDER '] = 'amitnk19@gmail.com'
app.config['MAIL_MAX_EMAILS '] =  None
#app.config[' MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False


mail = Mail(app)

@app.route('/')
def SignUp():
    msg = Message('Hey There',sender=('amitnk19@gmail.com') ,recipients=['geharo4594@hubopss.com'])
    msg.html = '<b>This is test mail sent from shabby\'s app. You don\'t have to reply.</b>'
    mail.send(msg)

    return 'has been sent'

if __name__ == '__main__':
   app.run(debug=True)