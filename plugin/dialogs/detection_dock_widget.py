# -*- coding: utf-8 -*-

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QFileDialog


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'detection_dock_widget.ui'))


class DetectionDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("DetectionDockWidget")
        self.setWindowTitle("Object detector")
        self.setFixedHeight(200)
        
    def get_progress_bar(self):
        return self.progressBar