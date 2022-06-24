# PROFILE="/c/Users/Богдан/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins"
cd plugin
pb_tool compile
cd ..

PROFILE="/home/skeptlk/.local/share/QGIS/QGIS3/profiles/default/python/plugins"
rm -rf $PROFILE/object_detector*
cp -r ./plugin $PROFILE/object_detector_plugin
echo "Plugin deployed successfully!"