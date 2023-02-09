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
def hello_world():
    photo_name = 'm-1.jpg'
    image = Image.open(photo_name)
    data=io.BytesIO()
    image.save(data,"JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    return render_template("Name.html",photo_name=encoded_img_data.decode('UTF-8'))

@app.route('/get_salary', methods = ["GET", "POST"])
def salary_input():
    return render_template('get_salary.html')

@app.route('/salary', methods = ["POST"])
def salary():
    df_op = pd.DataFrame()
    sal = request.form["sal"].isdigit()
    df = pd.read_csv("data-1.csv", converters={'income': int})
    df['income'] = df['income'].fillna(0)
    #df['income'] = pd.to_numeric(df['income'])
    df_op = df.loc[(df['income'] >= 0) & (df['income'] <= sal)]
    return render_template('salary.html',tables = [df_op.to_html()], titles=['name','income','comments'])

@app.route('/nameinc', methods = ["GET", "POST"])
def nameinc_input():
    return render_template('nameinc.html')

@app.route('/update', methods = ["GET", "POST"])
def nameinc():
    df = pd.read_csv("data-1.csv")
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
    photo_list = ['m-1.jpg','b-1.jpg']
    N = 'dar.jpg'
    df.loc[df.picture == ' ', ['picture']] = N
    for p in photo_list:   
            image = Image.open(p)
            data=io.BytesIO()
            image.save(data,"JPEG")
            enc_img = base64.b64encode(data.getvalue())
            #df_op['Picture_new']=enc_img.decode('UTF-8')
            enc_img = base64.b64encode(data.getvalue())
            
            return render_template('picture.html', photo_list = enc_img.decode('UTF-8'))


if __name__ == "__main__":
 app.run(host='0.0.0.0', port=8000, debug = True)