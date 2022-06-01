from flask import Request, Flask, redirect
import os


def detect_handler(app: Flask, request: Request):
  app.logger.info(request.files)
  app.logger.info(request.headers)
  file = request.files['uploaded']
  if file.filename == '':
    return redirect('/')
  if file:
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
