import os
import json
import sys
from os.path import dirname
from pyrevit import HOST_APP

sys.path.append(dirname(dirname(dirname(__file__))))

model = __models__[0]
uidoc = HOST_APP.uiapp.OpenAndActivateDocument(model)

import revitron

configFile = os.getenv('REVITRON_ANALYSE_CFG_FILE')
file = open(configFile)
config = revitron.AttrDict(json.load(file))
file.close()

ma = revitron.ModelAnalyser(config.database, config.providers)
ma.snapshot()