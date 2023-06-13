from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from PIL import Image
import csv
import pandas as pd
from PIL import Image
import base64
import io
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO
from IPython.display import HTML


app = Flask(__name__)
app = Flask(__name__, static_folder='static', static_url_path='')

app.config.from_pyfile('config.py')
account = app.config['ACCOUNT_NAME']   # Azure account name
key = app.config['ACCOUNT_KEY']      # Azure Storage account access key  
connect_str = app.config['CONNECTION_STRING']
container = app.config['CONTAINER'] # Container name
allowed_ext = app.config['ALLOWED_EXTENSIONS'] # List of accepted extensions

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

@app.route('/', methods = ["GET","POST"])
def index():
    df = pd.read_csv("./static/people.csv",on_bad_lines='skip')
    return render_template("index.html",tables=[df.to_html()],titles=['Name','State','Salary','Grade','Room','Telnum','Picture','Keywords'])
    #return render_template("index.html")

# def Name():
#     photo_name = '../car.jpg'
#     image = Image.open(photo_name)
#     data=io.BytesIO()
#     image.save(data,"JPEG")
#     encoded_img_data = base64.b64encode(data.getvalue())
#     p = encoded_img_data.decode('UTF-8')
#     return render_template("Name.html",photo_name=p)
@app.route('/name',methods = ["GET","POST"])
def name():
    df = pd.read_csv("./static/people.csv",on_bad_lines='skip')
    name = request.form["name"]
    for i in df["Name"]:
        if i==name:
            p=df[df["Name"]==name]["Picture"].values[0]
            return render_template("index.html",tables=[df.to_html()],titles=['Name','State','Salary','Grade','Room','Telnum','Picture','Keywords'],photo_name=p)
    return render_template("index.html",tables=[df.to_html()],titles=['Name','State','Salary','Grade','Room','Telnum','Picture','Keywords'],error="Wrong name,Please input again!!!")
@app.route('/get_salary', methods = ["GET", "POST"])
def salary_input():
    return render_template('get_salary.html')

@app.route('/salary', methods = ["POST"])
def salary():
    df_op = pd.DataFrame()
    sal = request.form["sal"]
    sal1=request.form["sal1"]
    df = pd.read_csv("./static/people.csv",on_bad_lines='skip')
    df_op = df.loc[(df["Salary"]>=sal) & (df["Salary"]<=sal1)]
    print(df_op["Picture"].values)
    return render_template('salary.html',tables = [df_op.to_html()], titles=['Name','State','Salary','Grade','Room','Telnum','Picture','Keywords'],photo_name=df_op["Picture"].values)
@app.route('/get_update', methods = ["GET", "POST"])
def update_input():
    return render_template('get_update.html')
@app.route('/get_delete', methods = ["GET", "POST"])
def delete_input():
    return render_template('get_delete.html')

@app.route('/update', methods = ["GET", "POST"])
def update():
    df = pd.read_csv("./static/people.csv",on_bad_lines='skip')
    name=request.form["name"]
    sal=request.form["sal"]
    word=request.form["word"]
    index=df.loc[df["Name"]==name].index
    if index.size==0:
        error="Wrong name,Please enter again!!!!"
        return render_template('get_update.html',errors=error) 
    if sal!="":
        df.loc[index,"Salary"]=sal
    if word!="":
        df.loc[index,"Keywords"]=word
    inf="Update success!!!!!"
    return render_template('update.html',tables=[df.to_html()],titles=['Name','State','Salary','Grade','Room','Telnum','Picture','Keywords'],info=inf)
@app.route('/delete', methods = ["GET", "POST"])
def delete():
    df = pd.read_csv("./static/people.csv",on_bad_lines='skip')
    name=request.form["name"]
    index=df.loc[df["Name"]==name].index
    if index.size==0:
        error="Wrong name,Please enter again!!!!"
        return render_template('get_delete.html',errors=error) 
    df_new=df.drop(index[0])
    inf="delete success!!!!!"
    return render_template('delete.html',tables=[df_new.to_html()],titles=['Name','State','Salary','Grade','Room','Telnum','Picture','Keywords'],info=inf)


    
    
 
if __name__ == "__main__":
    app.run(debug = True)
