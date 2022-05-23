from qgis.core import QgsTask, QgsMessageLog, Qgis, \
  QgsNetworkAccessManager, QgsNetworkReplyContent
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from qgis.PyQt.QtCore import QUrl

class DetectorHttpProvider():
  SERVER_URL = 'http://localhost:5000'
  DETECT_PATH = '/api/v0/detect'
  
  progress = 0.0
  
  def __init__(self, raster_path: str, on_finish):
    self.raster_path = raster_path
    self.on_finish = on_finish
    self.net_manager = QNetworkAccessManager()

  def post_raster(self):
    # todo: handle file open error
    file = open(self.raster_path, 'rb')
    url = self.SERVER_URL + self.DETECT_PATH;
    request = QNetworkRequest(QUrl(url))
    
    bound = b"output"
    
    data = bytearray()
    data += b'--' + bound + b'\r\n'
    data += b'Content-Disposition: form-data; name="uploaded"; filename="output.tif"\r\n';
    data += b'Content-Type: image/tif\r\n\r\n'
    data += bytearray(file.read())
    data += b'\r\n'
    data += b'--' + bound + b'--\r\n'
    
    request.setRawHeader(b"Content-Type", b"multipart/form-data; boundary=" + bound)
    request.setRawHeader(b"Content-Length", bytearray(len(data)))
    
    self.reply = self.net_manager.post(request, data)
    self.reply.uploadProgress.connect(self.post_raster_upload_progress)
    self.reply.finished.connect(self.post_raster_finished)
    
    QgsMessageLog.logMessage("HTTP provider: request sent")    

  def post_raster_upload_progress(self, sent: int, total: int):
    if total > 0:
      self.progress = 100.0 * sent / total
      QgsMessageLog.logMessage("HTTP provider: sent {} of {} bytes".format(sent, total))
    
  def post_raster_finished(self):
    self.on_finish(self.reply.readAll())
    QgsMessageLog.logMessage("HTTP provider: completed!")
    
    