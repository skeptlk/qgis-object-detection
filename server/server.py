
from flask import Flask, request, redirect
import os
import time
import model.unet_detector
from handlers import detect_handler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/")
def index_page():
  time.sleep(10)
  return "<h2>Object detector plugin</h2>" + \
    "<p>This is the main page of object detection plugin delayed by 3 seconds</p>";

@app.route("/hello")
def hello_page():
  return "<h2>Hello</h2>"

@app.route("/api/v0/detect", methods=['POST'])
def api_detect():
  return detect_handler(app, request)

