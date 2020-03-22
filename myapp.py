from flask import Flask,render_template,request,url_for,redirect,jsonify
from flask_pymongo import PyMongo
from flask_wtf import RecaptchaField,FlaskForm
import bcrypt
import socket   
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret'
app.config['MONGO_DBNAME']='loginData'
app.config['MONGO_URI']='mongodb+srv://sumit:sumit@cluster0-74s1u.mongodb.net/loginData?retryWrites=true&w=majority'
app.config['RECAPTCHA_PUBLIC_KEY']='6Lcz8-IUAAAAADkCP9hwe5uzYp3yu8Ez8YmK2gXC'
app.config['RECAPTCHA_PRIVATE_KEY']='6Lcz8-IUAAAAAPm8olKS8eMOw5VIa-Cj2KSL-faO'

mongo=PyMongo(app)

class Recaptcha(FlaskForm):
        recaptcha = RecaptchaField()

def getIP():
        ip = request.remote_addr
        if(ip=="127.0.0.1"):
                ip = socket.gethostbyname(socket.gethostname())
        return ip

@app.route("/login/",methods=["POST","GET"])

def login():
        form = Recaptcha()
        ip=getIP()
        if request.method=="POST":
                print("Login request from IP:"+ip)
                username=request.form["name"]
                useremail=request.form["email"]
                userpass=bcrypt.hashpw(request.form["password"].encode('utf-8'),bcrypt.gensalt())
                users = mongo.db.users
                users.insert({"Name":username,"Email":useremail,"Password":userpass,"IPADDRESS":ip})
                print("User Data successfully stored to database for username : "+username)
        attempts=(len(list(mongo.db.users.find({"IPADDRESS":ip}))))
        print(attempts)
        if attempts>=3:
                return render_template("login.html",form = form)
        else:
                return render_template("login.html",form = None)

@app.route("/users/")
def users():
        users = mongo.db.users
        userData="<table border='1px'><tr><th>Name</th><th>Email</th></tr>"
        for user in mongo.db.users.find():
                userData=userData+"<tr><td>"+(user["Name"]+"</td><td>"+user["Email"]+"</td></tr>")
                print("User Data populated for : "+user["Name"])
        userData+="</table>"
        return userData

if __name__=="__main__":
	app.run(host='0.0.0.0',debug=True)
