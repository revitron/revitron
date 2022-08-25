import sys
import os
from os.path import dirname
from pyrevit import HOST_APP

sys.path.append(dirname(dirname(dirname(__file__))))

import revitron
from cli import getEnv, getLogFromEnv
from cli.config import Config

env = getEnv()
log = getLogFromEnv().write
config = Config(detach=False)

revitron.DOC = HOST_APP.uiapp.Application.OpenDocumentFile(
    config.modelPath, config.openOptions
)

try:
	syncOptions = revitron.DB.SynchronizeWithCentralOptions()
	syncOptions.Compact = True
	syncOptions.Comment = 'Compact model'
	syncOptions.SaveLocalAfter = False
	syncOptions.SaveLocalBefore = False
	revitron.DOC.SynchronizeWithCentral(
	    revitron.DB.TransactWithCentralOptions(), syncOptions
	)
	log('Synching finished successfully')
except Exception as e:
	log('Synching failed')
	log(str(e))

revitron.DOC.Close(False)