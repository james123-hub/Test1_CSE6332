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
    photo_name = 'dave.jpg'
    image = Image.open(photo_name)
    data=io.BytesIO()
    image.save(data,"JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    p = encoded_img_data.decode('UTF-8')
    return render_template('Name.html',photo_name=p)

@app.route('/user', methods = ["POST"])
def user():
    df = pd.read_csv("data-1.csv",on_bad_lines='skip')
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

@app.route('/get_salary', methods = ["GET", "POST"])
def salary_input():
    return render_template('get_salary.html')

@app.route('/salary', methods = ["POST"])
def salary():
    
    df_op = pd.DataFrame()
    sal = request.form["sal"].isdigit()
    sal1 = request.form["sal1"].isdigit()
    df = pd.read_csv("data-1.csv",on_bad_lines='skip')
    #df = pd.read_csv("data-1.csv", converters={'income': int})
    df['income'] = df['income'].fillna(0)
    #df['income'] = pd.to_numeric(df['income'])
    df_op = df.loc[(df['income'] >= sal) & (df['income'] <= sal1)]
    return render_template('salary.html',tables = [df_op.to_html()], titles=['name','income','comments'])

@app.route('/nameinc', methods = ["GET", "POST"])
def nameinc_input():
    return render_template('nameinc.html')

@app.route('/update', methods = ["GET", "POST"])
def nameinc():
    df = pd.read_csv("data-1.csv",on_bad_lines='skip')
    df_op = pd.DataFrame()
    name = request.form["name"]
    inc = request.form["sal1"]
    comments = request.form["text"]
    #df_op = df.loc[df.name == name, ['name','income', 'comments']] = name,inc, comments
    df.loc[df.name == name, ['name','income', 'comments']] = name,inc, comments
    df.to_csv ("data-1.csv", index = None, header=True)
    return render_template('update.html',name=name,tables=[df.to_html()],titles=['name','income','comments'],comments=comments)

@app.route('/picture', methods = ["GET","POST"])
def picture():

    
    df = pd.read_csv("data-1.csv",on_bad_lines='skip')
    df.loc[df.picture == ' ', 'picture'] = 'No_Picture.jpg'
    df.loc[df.picture == 'Nan', 'picture'] = 'No_Picture.jpg'
    df.to_csv ("data-1.csv", index = None, header=True)
    pdict = zip(df.name,df.picture)
    pdict=dict(pdict)
    return render_template("picture.html",tables=[df.to_html()],titles=['name','income','comments'],image_name=pdict)

@app.route('/upload', methods = ["GET","POST"])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        #if img and allowed_file(img.filename):
        filename = secure_filename(img.filename)
        img.save(filename)
        blob_client = blob_service_client.get_blob_client(container = container, blob = filename)
        with open(filename, "rb") as data:
                try:
                    blob_client.upload_blob(data, overwrite=True)
                    #msg = "Upload Done ! "
                except:
                    pass
        #os.remove(filename)
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug = True)
