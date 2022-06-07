
from flask import Flask, request, redirect
import os
from model.unet_detector import UnetDetector
from server.handlers.detect_handler import detect_handler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.extensions['BUILDING_DETECT_MODEL'] = UnetDetector()

@app.route("/")
def index_page():
  return "<h2>Object detector plugin</h2>" + \
    "<p>This is the main page of object detection plugin</p>";

@app.route("/api/v0/detect", methods=['POST'])
def api_detect():
  return detect_handler(app, request)

