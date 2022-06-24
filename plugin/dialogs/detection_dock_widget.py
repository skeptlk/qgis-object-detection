# -*- coding: utf-8 -*-

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QStandardItemModel, QStandardItem

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'detection_dock_widget.ui'))

class DetectionDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    def __init__(self, parent=None):
        super(DetectionDockWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("MyDetectionDockWidgetTest123")
        self.setWindowTitle("Object detector")
        self.setMinimumSize(50, 50)
        
        detectionTypes = [
            ["Buildings", True, True],
            ["Roads", False, False],
            ["Water bodies", False, False],
            ["Ships", False, False],
            ["Planes", False, False],
        ]

        model = QStandardItemModel();
        
        for (name, checkable, checked) in detectionTypes:
            item = QStandardItem()
            item.setText(name)
            item.setCheckable(checkable)
            item.setCheckState(Qt.Checked if checked else Qt.Unchecked)
            model.appendRow(item)

        self.detectionTypesListView.setModel(model)
        
    def get_progress_bar(self):
        return self.progressBar