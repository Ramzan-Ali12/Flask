from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
# from flask.ext import excel
# from flask import excel
from flask import Flask, render_template, url_for, redirect
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import pandas as pd
import os
import io


#Database file
db_path=os.path.join(os.path.dirname(__file__))
db_uri='sqlite:///'+os.path.join(db_path,"data.db")
app = Flask(__name__)
# encrypt for passward
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'

# *** Flask configuration
 
# Define folder to save uploaded files to process further
# UPLOAD_FOLDER = '/upload/data'
 
# Define allowed files
ALLOWED_EXTENSIONS = {'csv','XLS','txt'}
 
# db.create_all()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    city  =db.Column(db.String(80),unique=True) 
    def __repr__(self):
        return '<User %r>' % self.username  
# db.create_all()

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signupdata",methods=['GET','POST'])
def signupdata():
    if request.method =='POST':
        name= request.form.get('username')
        password=request.form.get('pass')
        city=request.form.get('city')
        entry=User(username=name,password=password,city=city)
        db.session.add(entry)
        db.session.commit()
        return render_template("login.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/logindata",methods=['GET','POST'])
def logindata():
    if request.method =='POST':
        username = request.form['username']
        passward = request.form['pass']
        us=User.query.filter_by(username=username,password=passward).first()
        if us:
            return render_template("index.html")
                   
@app.route('/showdata',methods=("POST","GET"))
def showdata():
    if request.method == 'POST':
        # upload file flask
        uploaded_df = request.files['uploaded-file']
        # Save the uploaded file in the database
        uploaded_df.save(os.path.join("upload/data/", secure_filename(uploaded_df.filename)))
        
        # print("**************************************")
        # print(uploaded_df)
        # filesList = os.listdir('upload/data/')
        # print(filesList)
        if uploaded_df.filename.endswith('csv'):
            uploaded_df = pd.read_csv("upload/data/"+ uploaded_df.filename)
        elif uploaded_df.filename.endswith('xlsx'):
            uploaded_df = pd.read_excel("upload/data/"+uploaded_df.filename)
        
        # print(uploaded_df)
        # pandas dataframe to html table flask
    uploaded_df_html = uploaded_df.to_html()
    # print(uploaded_df)
    # pandas dataframe to html table flask
    # uploaded_df_html = uploaded_excel.to_html()
    return render_template('temprary.html',data_var = uploaded_df_html)

@app.route('/visualization')  
def visualization():
    return render_template("visualize.html")

if __name__ == "__main__":
    app.run(debug=True)
