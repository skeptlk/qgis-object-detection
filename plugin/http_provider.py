from qgis.core import QgsTask, QgsMessageLog, Qgis, \
  QgsNetworkAccessManager, QgsNetworkReplyContent
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkAccessManager

class DetectTask():
  SERVER_URL = 'http://localhost:5000'
  DETECT_PATH = '/api/v0/detect'
  
  def __init__(self):
    self.net_manager = QNetworkAccessManager()

  def post_extent(self, extent_path):
    path = self.SERVER_URL + self.DETECT_PATH;
    pass
  
