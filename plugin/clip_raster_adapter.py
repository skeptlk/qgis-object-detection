

from .clip_raster_algorithm import ClipRaster

from qgis.core import (QgsMessageLog,
                       QgsApplication,
                       QgsMapLayer,
                       QgsProcessingProvider,
                       QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingParameterDefinition,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingOutputRasterLayer,
                       QgsProcessingOutputPointCloudLayer,
                       QgsProcessingOutputMapLayer,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingFeedback,
                       QgsProcessingContext,
                       QgsRuntimeProfiler,
                       QgsRectangle,
                       QgsRasterLayer)
from processing.gui.AlgorithmExecutor import execute
from processing.tools import dataobjects


class ClipRasterAdapter():
    
    @staticmethod
    def run(
        extent: QgsRectangle, 
        input: QgsRasterLayer,
        onFinish = None
    ):
        feedback = QgsProcessingFeedback()
        context = dataobjects.createContext(feedback)
        if context.feedback() is None:
            context.setFeedback(feedback)
        alg = ClipRaster()
        output = QgsProcessingParameterRasterDestination('OUTPUT').generateTemporaryDestination()
        parameters = {
            'PROJWIN': extent,
            'INPUT': input,
            'OUTPUT': output,
            'OVERCRS': True
        }
        ret, results = execute(alg, parameters, context,
                               feedback, catch_exceptions=False)

        if ret:
            feedback.pushInfo('Results: {}'.format(results))

            if onFinish is not None:
                onFinish(alg, context, feedback)
            else:
                # auto convert layer references in results to map layers
                for out in alg.outputDefinitions():
                    if out.name() not in results:
                        continue

                    if isinstance(out, (QgsProcessingOutputVectorLayer, QgsProcessingOutputRasterLayer, QgsProcessingOutputPointCloudLayer, QgsProcessingOutputMapLayer)):
                        result = results[out.name()]
                        if not isinstance(result, QgsMapLayer):
                            # transfer layer ownership out of context
                            layer = context.takeResultLayer(result)
                            if layer:
                                # replace layer string ref with actual layer (+ownership)
                                results[out.name()] = layer
                    elif isinstance(out, QgsProcessingOutputMultipleLayers):
                        result = results[out.name()]
                        if result:
                            layers_result = []
                            for l in result:
                                if not isinstance(result, QgsMapLayer):
                                    # transfer layer ownership out of context
                                    layer = context.takeResultLayer(l)
                                    if layer:
                                        layers_result.append(layer)
                                    else:
                                        layers_result.append(l)
                                else:
                                    layers_result.append(l)

                            results[out.name()] = layers_result  # replace layers strings ref with actual layers (+ownership)

        else:
            msg = "There were errors executing the algorithm."
            feedback.reportError(msg)
            raise QgsProcessingException(msg)
        return results
