import revitron
from cli import App, getLogFromEnv

log = getLogFromEnv().write

revitron.DOC = App.open(False)

if revitron.Document().synchronize(compact=True, comment='Compact model'):
	log('Synching finished successfully')
else:
	log('Synching failed')

revitron.DOC.Close(False)