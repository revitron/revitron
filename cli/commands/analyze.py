import revitron
from cli import App, Config, getLogFromEnv

config = Config()
cliLog = getLogFromEnv()

revitron.DOC = App.open(True)

analyzer = revitron.ModelAnalyzer(config.file, cliLog)
analyzer.snapshot()

revitron.DOC.Close(False)