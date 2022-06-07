from flask import Request, Flask, redirect
from model.unet_detector import UnetDetector
import os


def detect_handler(app: Flask, request: Request):
  app.logger.info(request.files)
  app.logger.info(request.headers)
  file = request.files['uploaded']
  if file.filename == '':
    return redirect('/')
  if file is None:
    return redirect('/')
  saved_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
  file.save(saved_path)
  detector = app.extensions['BUILDING_DETECT_MODEL']
  wkt = detector.detect(saved_path, app)

  return wkt

 