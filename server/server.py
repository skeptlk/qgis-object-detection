
from flask import Flask, request, redirect, url_for
import os


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
  return "POLYGON ((533193.1015783922 174038.23070064266, 533193.0385603837 174038.41525338194, 533194.6229692716 174038.95627105064, 533194.6983712668 174038.7354509218, 533194.879708215 174038.79737085517, 533195.0604846688 174038.26795409713, 533193.0052700456 174037.56617349468, 533192.8121096052 174038.1318576422, 533193.1015783922 174038.23070064266))"

