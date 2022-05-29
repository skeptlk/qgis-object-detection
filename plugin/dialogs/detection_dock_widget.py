# -*- coding: utf-8 -*-

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QFileDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'detection_dock_widget.ui'))

class DetectionDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    def __init__(self, parent=None):
        super(DetectionDockWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("MyDetectionDockWidgetTest")
        self.setWindowTitle("Object detector")
        self.setMinimumSize(50, 50)
        
    def get_progress_bar(self):
        return self.progressBar