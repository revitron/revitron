import os
import json
import sys
from os.path import dirname
from pyrevit import HOST_APP

sys.path.append(dirname(dirname(dirname(__file__))))

import revitron
import cli

cli.CliLog.stdout()

modelPath = revitron.DB.ModelPathUtils.ConvertUserVisiblePathToModelPath(__models__[0])

worksetConfig = revitron.DB.WorksetConfiguration(
    revitron.DB.WorksetConfigurationOption.OpenAllWorksets
)

openOptions = revitron.DB.OpenOptions()
openOptions.SetOpenWorksetsConfiguration(worksetConfig)
openOptions.DetachFromCentralOption = revitron.DB.DetachFromCentralOption.DetachAndPreserveWorksets

uidoc = HOST_APP.uiapp.OpenAndActivateDocument(modelPath, openOptions, False)

reload(revitron)

configFile = os.getenv('REVITRON_ANALYSE_CFG_FILE')
file = open(configFile)
config = revitron.AttrDict(json.load(file))
file.close()

analyzer = revitron.ModelAnalyzer(config.database, config.providers, config.model)
analyzer.snapshot()