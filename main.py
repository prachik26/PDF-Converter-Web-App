from distutils.log import debug
from typing import Tuple
from unittest import result
from flask import Flask
from flask import request,render_template, redirect, url_for, send_file, flash, session, send_from_directory
from flask_wtf import FlaskForm
from requests import Session
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import os, sys
from fpdf import FPDF
from docx2pdf import convert
import pdfkit


config = pdfkit.configuration(wkhtmltopdf = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
app=Flask(__name__)
sess=Session()

#UPLOAD_FOLDER = 'uploads/'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOADER_FOLDER=''
app.config['UPLOADER_FOLDER']=UPLOADER_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'docx', 'py', 'cpp', 'html'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index',methods=['GET','POST'])

def index():
    if request.method=="POST":
        file=request.files['filename']
        if file.filename == '':
            #flash('No selected file')
            return "No selected file"
        if file.filename!='' and allowed_file(file.filename):
            file_ext=os.path.splitext(file.filename)[1]
            file.save(os.path.join(app.config['UPLOADER_FOLDER'],secure_filename(file.filename)))

            input_file=file.filename
            output_file=input_file.split(".")[0]+".pdf"
            if file_ext=='.html':
                pdfkit.from_file(input_file, output_file, configuration = config, verbose=True, options={"enable-local-file-access": True})
                print("="*50)
            elif file_ext=='.docx':
                convert(input_file)
            elif file_ext=='.py' or '.txt' or '.cpp': 
                pdff = FPDF()
                pdff.add_page()
                pdff.add_font("Arial", "", "arial.ttf", uni=True)
                pdff.set_font("Arial", size = 11)
                # open the text file in read mode
                f = open(input_file, "r")
                # insert the texts in pdf
                for x in f:
	                pdff.cell(200, 10, txt = x, ln = 1, align = 'L')
                
                pdff.output(output_file)
            else:
                pass
            pdf=input_file.split(".")[0]+".pdf"
            print(pdf)
            lis=pdf.replace(" ","=")
            #return redirect('/downloadfile/'+ output_file)
            return render_template("docx.html",variable=lis)
    return render_template("index.html")

@app.route('/docx',methods=['GET','POST'])
def docx():
    if request.method=="POST":
        lis=request.form.get('filename',None)
        lis=lis.replace("="," ")
        #send_from_directory(app.config["UPLOADER_FOLDER"], lis)
        return send_file(lis,as_attachment=True)
    return  render_template("index.html")

if __name__=='__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    #sess.init_app(app)
    app.run(debug=True, host='0.0.0.0')