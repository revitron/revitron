from pyrevit import HOST_APP
from cli.config import Config


class App():

	@staticmethod
	def open(detach=True):
		config = Config(detach)

		return HOST_APP.uiapp.Application.OpenDocumentFile(
		    config.modelPath, config.openOptions
		)