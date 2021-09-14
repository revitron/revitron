import os
import json
import sys
from os.path import dirname
from pyrevit import HOST_APP

sys.path.append(dirname(dirname(dirname(__file__))))

model = __models__[0]

import revitron

modelPath = revitron.DB.ModelPathUtils.ConvertUserVisiblePathToModelPath(model)
openOptions = revitron.DB.OpenOptions()
openOptions.DetachFromCentralOption = revitron.DB.DetachFromCentralOption.DetachAndPreserveWorksets

uidoc = HOST_APP.uiapp.OpenAndActivateDocument(modelPath, openOptions, False)

configFile = os.getenv('REVITRON_ANALYSE_CFG_FILE')
file = open(configFile)
config = revitron.AttrDict(json.load(file))
file.close()

analyzer = revitron.ModelAnalyzer(config.database, config.providers, config.model)
analyzer.snapshot()