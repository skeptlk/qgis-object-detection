PROFILE="/c/Users/Богдан/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins"
rm -rf $PROFILE/object_detector
cp -r ./plugin $PROFILE/object_detector
echo "Plugin deployed successfully!"