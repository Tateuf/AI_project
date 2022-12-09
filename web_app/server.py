from flask import Flask
from flask import render_template, request
import os
from werkzeug.utils import secure_filename
import digitRecognition

UPLOAD_FOLDER = os.path.join('static', 'uploads')

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/digit', methods=('GET', 'POST'))
def digit():
   img_filename=""
   guess = "waiting input"
   if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save("web_app/static/"+img_filename)
        guess = digitRecognition.digit_recognition("web_app/static/"+img_filename)
      #   # Storing uploaded file path in flask session
      #   session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
   
   return render_template('digit_check.html', preview = "static/"+img_filename, guess = guess)

@app.route('/crop')
def home():
   return render_template('crop.html', preview = "static/lorem_mandel.png")

@app.route('/box')
def boxGenerator(inputfile):
   boxed_img = "some future image"
   # boxed_img = cv2.boundingbox(inputfile)
   return boxed_img

if __name__ == '__main__':
   app.run()