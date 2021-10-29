import re
from flask import Flask, config ,render_template,request,redirect
import os
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.utils import secure_filename
from flask_mail import Mail
app = Flask(__name__)
with open("config.json","r") as c:
    params=json.load(c)["params"]
mail=Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER']=params["UPLOAD_LOCATION"]
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avtar=  db.Column(db.String(120), unique=True, nullable=False)
    pasw=  db.Column(db.String(120), unique=True, nullable=False)
@app.route("/sign",methods=['GET','POST'])
def sign():
    if request.method=='POST':
        name=request.form.get('user')
        passw=request.form.get('passw')
        email=request.form.get('email')
        f=request.files['file']
        f.filename=name+'.jpg'
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        enter=User(username=name,email=email,avtar=f.filename,pasw=passw)
        db.session.add(enter)
        db.session.commit()
    return render_template('index.html')
if __name__=="__main__":
    app.run(debug=True)
