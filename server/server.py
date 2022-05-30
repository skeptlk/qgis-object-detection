
from flask import Flask, request, redirect
import os
import model.unet_detector

print(os.environ.get('HELLO'))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/")
def index_page():
  return "<h2>Object detector plugin</h2>" + \
    "<p>This is the main page of object detection plugin</p>";

@app.route("/api/v0/detect", methods=['POST'])
def api_detect():
  app.logger.info("Look below: ")
  app.logger.info(request.files)
  app.logger.info(request.headers)
  file = request.files['uploaded']
  if file.filename == '':
    return redirect('/')
  if file:
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
  return 

