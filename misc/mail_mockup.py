from flask import Flask
from flask_mail import Mail,Message
import smtplib


app = Flask("DeutschKlar.rc")



app.config.update(
  DEBUG=True,
  #EMAIL SETTINGS
  MAIL_SERVER='smtp.gmail.com',
  MAIL_PORT=465,
  MAIL_USE_SSL=True,
  MAIL_USERNAME = 'DeutschKlar.rc',
  MAIL_PASSWORD = 'vfjy edir ovze eptu'
)
mail = Mail(app)

@app.route("/")
def home():
  try:
    msg = Message("Message Title Here", sender="deutschkalr.rc@gmail.com", recipients=["damour91919@gmail.com"])
    msg.body = "Sample Message Body Here"        
    msg.html = "<h1 style='color:green;'>Sample Message Body Here With HTML and CSS Style</h1>"
    
    with app.open_resource("3BP.pdf") as fp:
        msg.attach("3BP.pdf", "application/pdf", fp.read())
        
    mail.send(msg)
    return 'Mail Send Successfully'
    
  except Exception as e:
    print(str(e))
  return ""

if __name__=="__main__":
  app.run(debug=True)






'''
app.config["DEBUG"]=False
app.config["TESTING"]=False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="sekret_key"
app.config["MAIL_SERVER"]="smtp.gmail.com'"
app.config["MAIL_PORT"]=465
app.config["MAIL_USE_TLS"]=False
app.config["MAIL_USE_SSL"]=True
app.config["MAIL_DEBUG"]=False
app.config["MAIL_USERNAME"]="your_username@gmail.com"
app.config["MAIL_PASSWORD"]="your_app_password"
app.config["MAIL_DEFAULT_SENDER"]=None
app.config["MAIL_MAX_EMAILS"]=None
app.config["MAIL_SUPPRESS_SEND"]=False
app.config["MAIL_ASCII_ATTACHMENTS"]=False
'''
