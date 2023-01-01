from flask import Flask
from flask import render_template, request
import os
from werkzeug.utils import secure_filename
import digit_recognition
import character_recognition
import text_detection
import tesseract
from datetime import datetime
import json
import fitz
import base64

UPLOAD_FOLDER = os.path.join('static', 'uploads')

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

def fileUpload():
   file_names=[]
   input_filename=""
   if request.method == 'POST':
      # Upload file flask
      # Extracting uploaded data file name
      uploaded_file = request.files['uploaded-file']
      input_filename = secure_filename(uploaded_file.filename)
      # Upload file to database (defined uploaded folder in static path)
      uploaded_file.save("web_app/static/"+input_filename)
      file_names.append(input_filename)
      
      #convert to image if filetype is pdf
      if("pdf" in input_filename):
         file_names.pop(0)
         pdffile = "web_app/static/"+input_filename
         doc = fitz.open(pdffile)
         i = 0
         
         for page in doc:
            i += 1
            pix = page.get_pixmap()
            tpix = page.get_text()
            print(tpix)
            print("trololol")
            output = "web_app/static/"+input_filename[:-4]+"_" + str(i) + "_c.png"
            file_names.append(input_filename[:-4]+"_1_c.png")
            pix.save(output)
         
      
      return file_names

def logRegister(input_filename, guess):
   with open("web_app/logs.json",'r+') as file:
      # First we load existing data into a dict.
      file_data = json.load(file)
      # Join new_data with file_data inside emp_details
      record = {"date":str(datetime.now().date()),"time":str(datetime.now().time()),"file": input_filename,"content":str(guess)}
      file_data["history"].append(record)
      # Sets file's current position at offset.
      file.seek(0)
      # convert back to json.
      json.dump(file_data, file, indent = 4)

@app.route('/digit', methods=('GET', 'POST'))
def digit():
   input_filename = fileUpload()[-1]
   guess = "waiting input"
   guess = digit_recognition.digit_recognition("web_app/static/"+input_filename)
   logRegister(input_filename, guess)
   return render_template('digit_check.html', preview = "static/labeled_"+input_filename, guess = guess)

@app.route('/tesseract', methods=('GET', 'POST'))
def textTyped():
   guess = []
   files = fileUpload()
   for file in files:
      guess.append(tesseract.tesseract("web_app/static/"+file))
      logRegister(file, guess[-1])
      with open("web_app/static/"+file, "rb") as data_file:
         data = data_file.read()
      encoded_file = base64.b64encode(data).decode('utf-8')
   return render_template('digit_check.html', preview = "static/"+files[0], guess = guess, encoded_file = encoded_file )

@app.route('/emnist', methods=('GET', 'POST'))
def handwritten():
   input_filename = fileUpload()[-1]
   guess = "waiting input"
   guess = character_recognition.characterRecognition("web_app/static/"+input_filename)
   logRegister(input_filename, guess)
   return render_template('digit_check.html', preview = "static/labeled_"+input_filename, guess = guess)

@app.route('/box')
def boxGenerator(inputfile):
   text_detection.text_detection(img)
   boxed_img = "some future image"
   # boxed_img = cv2.boundingbox(inputfile)
   return boxed_img

if __name__ == '__main__':
   app.run()