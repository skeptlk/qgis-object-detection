# -*- coding: utf-8 -*-

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QFileDialog


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'export_layer_dialog_base.ui'))


class ExportLayerDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ExportLayerDialog, self).__init__(parent)
        self.setupUi(self)
        self.selectFileButton.clicked.connect(self.select_output_file)

    def set_layers(self, layers):
        self.layers = layers
        self.layerComboBox.clear()
        # # Populate the comboBox with names of all the loaded layers
        self.layerComboBox.addItems([layer.name() for layer in layers])

    def select_output_file(self):
        filename, _filter = QFileDialog.getSaveFileName(
            self, "Select output file", "", "*.csv"
        )
        self.filename = filename
        self.fileNameLineEdit.setText(filename)

    def get_selected_layer(self):
        selectedLayerIndex = self.layerComboBox.currentIndex()
        return self.layers[selectedLayerIndex].layer()