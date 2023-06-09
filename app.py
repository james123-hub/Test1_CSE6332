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
def Name():
    photo_name = 'car.jpg'
    image = Image.open(photo_name)
    data=io.BytesIO()
    image.save(data,"JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    p = encoded_img_data.decode('UTF-8')
    return render_template("Name.html",photo_name=p)

@app.route('/user', methods = ["POST"])
def user():
    df = pd.read_csv("q0c.csv",on_bad_lines='skip')
    name = request.form["name"]
    for i in df["name"]:
        if i !=name:
            next
        elif i ==name:
            pdict = zip(df.name,df.picture)
            pdict=dict(pdict)
            state = df[df["name"]==i]["class"].values[0]
            print("{}'s class is {}".format(i,state)) 
            photo_name = pdict[i]
            image = Image.open(photo_name)
            data=io.BytesIO()
            image.save(data,"JPEG")
            encoded_img_data = base64.b64encode(data.getvalue())
            return render_template('user.html',user=name,state=state,photo_name=encoded_img_data.decode('utf-8')) 
        return render_template('not_found.html')

@app.route('/get_room', methods = ["GET", "POST"])
def room_input():
    return render_template('get_room.html')

@app.route('/room', methods = ["POST"])
def room():
    
    df_op = pd.DataFrame()
    room = request.form["room"].isdigit()
    df = pd.read_csv("q0c.csv", converters={'room': int},on_bad_lines='skip')
    #df['income'] = df['income'].fillna(0)
    #df['income'] = pd.to_numeric(df['income'])
    df_op = df.loc[df['room'] == room]
    return render_template('room.html',tables = [df_op.to_html()], titles=['name','pic','descript'])
@app.route('/get_number', methods = ["GET", "POST"])
def number_input():
    return render_template('get_number.html')

@app.route('/number', methods = ["POST"])
def number():
    
    df_op = pd.DataFrame()
    min1 = request.form["min"].isdigit()
    max1=request.form["max"].isdigit()
    df = pd.read_csv("q0c.csv", converters={'teln': int},on_bad_lines='skip')
    #df['income'] = df['income'].fillna(0)
    #df['income'] = pd.to_numeric(df['income'])
    df_op = df.loc[(df['teln']>=min1)& (df['teln']<=max1)]
    return render_template('number.html',tables = [df_op.to_html()], titles=['name','teln','pic','descript'])
@app.route('/nameinc', methods = ["GET", "POST"])
def nameinc_input():
    return render_template('nameinc.html')

@app.route('/update', methods = ["GET", "POST"])
def nameinc():
    df = pd.read_csv("q0c.csv",on_bad_lines='skip')
    df_op = pd.DataFrame()
    teln = request.form["teln"]
    comments = request.form["text"]
    new_row={'room':'','teln':teln,'pic':'','descript':comments}
    #df_op = df.loc[df.name == name, ['name','income', 'comments']] = name,inc, comments
    df = df.append(new_row, ignore_index=True)
    df.to_csv ("q0c.cs", index = False)
    return render_template('update.html',tables=[df.to_html()],titles=['name','teln','pic','descript'])

@app.route('/picture', methods = ["GET","POST"])
def picture():

    
    df = pd.read_csv("q0c.csv",on_bad_lines='skip')
    df.loc[df.picture == ' ', 'picture'] = 'No_Picture.jpg'
    df.loc[df.picture == 'Nan', 'picture'] = 'No_Picture.jpg'
    df.to_csv ("q0c.csv", index = None, header=True)
    pdict = zip(df.name,df.picture)
    pdict=dict(pdict)
    return render_template("picture.html",tables=[df.to_html()],titles=['name','year','comments'],image_name=pdict)
 
if __name__ == "__main__":
    app.run(debug = True)
