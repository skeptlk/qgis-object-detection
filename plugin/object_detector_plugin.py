# -*- coding: utf-8 -*-
"""
/***************************************************************************
    ObjectDetectorPlugin
    -------------------
    begin                : 2022-04-15
    email                : sceptlc@bk.ru
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QLocale, QLocale, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject, Qgis, QgsRectangle, QgsCoordinateTransform, QgsVectorLayer, QgsFeature, QgsGeometry, QgsField
from qgis.gui import QgisInterface, QgsMapToolExtent

from .clip_raster_adapter import ClipRasterAdapter

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .dialogs.export_layer_dialog import ExportLayerDialog
import os.path


class ObjectDetectorPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface: QgisInterface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ObjectDetectorPlugin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Object Detector')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ObjectDetectorPlugin', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.
        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str
        :param text: Text that should be shown in menu items for this action.
        :type text: str
        :param callback: Function to be called when the action is triggered.
        :type callback: function
        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool
        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool
        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool
        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str
        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget
        :param whats_this: Optional text to show in the status bar when the mouse pointer hovers over the action.
        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.add_action(
            ':/plugins/object_detector_plugin/icon.png',
            text=self.tr(u'Detect objects'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.add_action(
            ':/plugins/object_detector_plugin/radar.png',
            text=self.tr(u'Select an area'),
            callback=self.set_input_extent_from_draw_on_canvas,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def set_input_extent_from_draw_on_canvas(self):
        canvas = self.iface.mapCanvas()
        if (canvas):
            self.map_tool_previous = canvas.mapTool()
            map_tool_extent = QgsMapToolExtent(canvas)
            map_tool_extent.extentChanged.connect(self.extent_drawn)
            map_tool_extent.deactivated.connect(self.map_tool_deactivated)
            self.map_tool_current = map_tool_extent
            canvas.setMapTool(map_tool_extent)

    def extent_drawn(self, extent: QgsRectangle):
        canvas = self.iface.mapCanvas()
        canvas.setMapTool(self.map_tool_previous)
        self.map_tool_previous = None
        self.set_input_extent(extent)

    def map_tool_deactivated(self):
        self.map_tool_previous = None

    def set_input_extent(self, extent: QgsRectangle):
        active_layer = self.iface.activeLayer()
        
        # make post request
        vl = QgsVectorLayer("Polygon", "temp", "memory")
        pr = vl.dataProvider()
        pr.addAttributes([QgsField("id", QVariant.Int)])
        vl.updateFields()

        f = QgsFeature()
        
        wkt = extent.asWktPolygon()
        f.setGeometry(QgsGeometry.fromWkt(wkt))
        f.setAttributes([1])

        pr.addFeature(f)
        vl.updateExtents()
        QgsProject.instance().addMapLayer(vl)
        
        map_crs = self.iface.mapCanvas().mapSettings().destinationCrs()
        ct = QgsCoordinateTransform(
            map_crs, active_layer.crs(), QgsProject.instance())
        ct.setBallparkTransformsAreAppropriate(True)
        extent = ct.transformBoundingBox(extent)
        self.extent = extent

        self.show_extent_message(extent)

        # todo: check that raster layer is selected
        res = ClipRasterAdapter.run(
            extent,
            active_layer
        )

        self.iface.messageBar().pushMessage(
            "Title", "{}".format(res), level=Qgis.Success, duration=10)

    def show_extent_message(self, extent: QgsRectangle):
        # get dimensions of extent
        self.iface.messageBar().pushMessage(
            "Title",
            "You selected extent: ({0})".format(extent.asWktPolygon()),
            level=Qgis.Success,
            duration=10
        )

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&Object Detector'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = ExportLayerDialog()

        # Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()
        # Clear the contents of the comboBox from previous runs
        self.dlg.set_layers(layers)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            self.export_to_csv(self.dlg.filename)
            self.iface.messageBar().pushMessage(
                "Success", "Output file written at " + self.dlg.filename,
                level=Qgis.Success, duration=3
            )

    def export_to_csv(self, filename):
        with open(filename, 'w') as output_file:
            selectedLayer = self.dlg.get_selected_layer()
            fieldnames = [field.name() for field in selectedLayer.fields()]
            # write header
            line = ','.join(name for name in fieldnames) + '\n'
            output_file.write(line)
            # wirte feature attributes
            for f in selectedLayer.getFeatures():
                line = ','.join(str(f[name]) for name in fieldnames) + '\n'
                output_file.write(line)
