import sys
from os.path import dirname
from pyrevit import HOST_APP

sys.path.append(dirname(dirname(dirname(__file__))))

import revitron
from cli import getLogFromEnv
from cli.config import Config

config = Config()
cliLog = getLogFromEnv()

revitron.DOC = HOST_APP.uiapp.Application.OpenDocumentFile(
    config.modelPath, config.openOptions
)

analyzer = revitron.ModelAnalyzer(config.file, cliLog)
analyzer.snapshot()

revitron.DOC.Close(False)