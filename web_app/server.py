from flask import Flask
from flask import render_template, request
import os
from werkzeug.utils import secure_filename
import flask_resize

UPLOAD_FOLDER = os.path.join('static', 'uploads')

app = Flask(__name__)
resize = flask_resize.Resize(app)

app.config['UPLOAD_FOLDER'] = "/static/uploads"
app.config['RESIZE_URL'] = '/static/cropped'
app.config['RESIZE_ROOT'] = '/static'

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/digit', methods=('GET', 'POST'))
def digit():
   img_filename=""
   if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save("web_app/static/"+img_filename)
      #   # Storing uploaded file path in flask session
      #   session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
   return render_template('digit_check.html', preview = "static/"+img_filename)

# def uploadFile():
#     if request.method == 'POST':
#         # Upload file flask
#         uploaded_img = request.files['uploaded-file']
#         # Extracting uploaded data file name
#         img_filename = secure_filename(uploaded_img.filename)
#         # Upload file to database (defined uploaded folder in static path)
#         uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
#       #   # Storing uploaded file path in flask session
#       #   session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
 
#         return render_template('index_upload_and_show_data_page2.html')

if __name__ == '__main__':
   app.run()