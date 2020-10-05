from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask (__name__)

#condigure db
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:dameunpass@localhost/flaskapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False


db= SQLAlchemy(app)
ma= Marshmallow(app)


class User(db.Model):
    name= db.Column(db.String(20), unique=True)
    email= db.Column(db.String(40), primary_key=True)

    def __init__(self, name, email):
        self.name= name
        self.email=email
        
db.create_all()

class UserSchema(ma.Schema):
    class Meta:
        fields=('name', 'email')

user_schema= UserSchema()
users_schema= UserSchema(many=True)



@app.route('/', methods=[ 'GET','POST'])
def index():
    if request.method=='POST':
        #fetch data
        userDetails= request.form
        name= userDetails['name']
        email= userDetails['email']
        new_user= User(name, email)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)  
    return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True)
    