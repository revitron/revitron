"""
The ``forge`` submodule contains a collection of useful utility classes that help developers to interact 
with **BIM 360** models using the `Forge API <https://forge.autodesk.com/en/docs/data/v2/developers_guide/overview/>`_.
"""
import requests
import os.path
import System
from abc import ABCMeta
from pyrevit import HOST_APP


class ForgeAppAuthenticator:
	"""
	This class allows for authenticating API requests using a *client Id* and a *client secret* that both can 
	be provided by custom apps. You can find a quick tutorial about how to create a custom app in order to 
	authenticate `here <https://forge.autodesk.com/en/docs/oauth/v1/tutorials/create-app/>`_.
	"""

	def __init__(self, clientId, clientSecret):
		"""
		Init an app authenticator in order to get a *token* that can be used to authenticate Forge API requests,
		based on a client Id and client secret that belong to a custom app.

		Args:
			clientId (string): The *client Id* of your custom app
			clientSecret (string): The *client secret* of your custom app
		"""
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		data = {
		    'client_id': clientId,
		    'client_secret': clientSecret,
		    'grant_type': 'client_credentials',
		    'scope': 'data:read'
		}
		req = requests.post(
		    'https://developer.api.autodesk.com/authentication/v1/authenticate',
		    data=data,
		    headers=headers
		)
		responseData = req.json()
		self._token = responseData['access_token']

	@property
	def token(self):
		"""
		The authentication token that can be used to authenticate API requests using other Revitron Forge utilities.

		Returns:
			string: The token
		"""
		return self._token


class AbstractForgeUtil(object):
	"""
	An abstract Forge API utility class that can be used as a base class for Forge API helper classes. 
	Note that this is an abstract class that should not be used directly.
	"""

	__metaclass__ = ABCMeta

	def __init__(self, token):
		"""
		Basic class initialization.

		Args:
			token (string): An authentication token provided by a :class:`ForgeAppAuthenticator` instance
		"""
		self.token = token

	@property
	def _authHeader(self):
		"""
		The authorization header that can be used to authenticate API requests.

		Returns:
			dict: A header dict
		"""
		return {'Authorization': 'Bearer {}'.format(self.token)}


class ForgeProjectFinder(AbstractForgeUtil):
	"""
	This class helps to find a **BIM 360** project based on a project name.
	"""

	def __init__(self, projectName, token):
		"""
		Init a new project finder instance.

		Args:
			projectName (string): The name of a project that is used as name in the **BIM 360** project list
			token (string): An authentication token provided by a :class:`ForgeAppAuthenticator` instance
		"""
		self.projectName = projectName
		self.token = token
		self.project = self._getProject()

	def _getHubs(self):
		"""
		Get all hubs that are accessible using the provided token.

		Returns:
			list: A list of hub Ids
		"""
		req = requests.get(
		    'https://developer.api.autodesk.com/project/v1/hubs',
		    headers=self._authHeader
		)
		responseData = req.json()
		items = responseData['data']
		hubs = []
		for item in items:
			if item['type'] == 'hubs':
				hubs.append(item['id'])
		return hubs

	def _getProjectsInHub(self, hubId):
		"""
		Get projects that are stored in a single hub.

		Args:
			hubId (string): A hub Id

		Returns:
			dict: A dict that uses project names as key and a nested dict with ``id`` and ``hub`` as value
		"""
		projects = dict()
		url = 'https://developer.api.autodesk.com/project/v1/hubs/{}/projects'.format(
		    hubId
		)
		req = requests.get(url, headers=self._authHeader)
		responseData = req.json()
		items = responseData['data']
		for item in items:
			if item['type'] == 'projects':
				name = item['attributes']['name']
				projects[name] = {'id': item['id'], 'hub': hubId}
		return projects

	def _getProjectsInAllHubs(self):
		"""
		Get all projects that are stored in all hubs.

		Returns:
			dict: A dict that uses project names as key and a nested dict with ``id`` and ``hub`` as value
		"""
		projects = dict()
		for hubId in self._getHubs():
			projects.update(self._getProjectsInHub(hubId))
		return projects

	def _getProject(self):
		"""
		Get the project Id and the hub Id that belog to the requested project name as a dict

		Returns:
			dict: A dict with ``id`` and ``hub`` of the requested project
		"""
		projects = self._getProjectsInAllHubs()
		if self.projectName in projects:
			return projects[self.projectName]

	@property
	def projectId(self):
		"""
		The project Id that is used to reference a project using the Forge API.

		Returns:
			string: The project Id
		"""
		return self.project['id']

	@property
	def hubId(self):
		"""
		The hub Id of a project that is used to reference a hub using the Forge API.

		Returns:
			string: The hub Id
		"""
		return self.project['hub']


class ForgeModelFinder(AbstractForgeUtil):
	"""
	This class helps to find a **BIM 360** model based on a *project name* and a *path* in order
	to collect all required properties to open and interact with a cloud-based model.

	Note:
		
		Note that you need to create a custom 
		`Forge app <https://forge.autodesk.com/en/docs/oauth/v1/tutorials/create-app/>`_ 
		in order to get a *client Id* and a *client secret* to be able to authenticate.
		

	The following example demonstrates how to find a model named ``model.rvt`` in a subfolder 
	called ``rvt`` inside of the ``Project Files`` folder within a **BIM 360** project and open it::

		clientId = 'xxxxx'
		clientSecret = '*****'
		token = revitron.ForgeAppAuthenticator(clientId, clientSecret).token
		model = revitron.ForgeModelFinder('My Project', 'rvt/model.rvt', token)
		doc = model.open()
	"""

	def __init__(self, projectName, path, token):
		"""
		Init a new model finder instance.

		Args:
			projectName (string): The name of a project that is used as name in the BIM-360 project list
			path (string): the path to the requested model within the ``Project Files`` folder
			token (string): An authentication token provided by a :class:`ForgeAppAuthenticator` instance
		"""
		project = ForgeProjectFinder(projectName, token)
		self.projectId = project.projectId
		self.hubId = project.hubId
		self.path = path
		self.token = token
		self.model = self._getModel()
		self.modelId = self.model['id']
		self.versions = self._getVersions()
		self.lastVersion = self.versions[-1]

	def _getProjectModelsFolder(self):
		"""
		Get the ``Project Files`` folder Id of a project.

		Returns:
			string: The folder Id
		"""
		url = 'https://developer.api.autodesk.com/project/v1/hubs/{hub}/projects/{project}/topFolders'
		req = requests.get(
		    url.format(hub=self.hubId,
		               project=self.projectId),
		    headers=self._authHeader
		)
		responseData = req.json()
		items = responseData['data']
		for item in items:
			if item['attributes']['name'] == 'Project Files':
				return item['id']

	def _getFolderContents(self, folderId):
		"""
		Get contents of a folder.

		Args:
			folderId (string): A folder Id

		Returns:
			dict: The contents data dict
		"""
		url = 'https://developer.api.autodesk.com/data/v1/projects/{project}/folders/{folder}/contents'
		req = requests.get(
		    url.format(project=self.projectId,
		               folder=folderId),
		    headers=self._authHeader
		)
		responseData = req.json()
		return responseData['data']

	def _getModelFolderContents(self):
		"""
		Get the contents of the parent folder of the requested model,

		Returns:
			dict: The contents data dict
		"""
		contents = self._getFolderContents(self._getProjectModelsFolder())
		folders = filter(len, os.path.dirname(self.path).split('/'))
		for folderName in folders:
			for item in contents:
				if item['type'] == 'folders':
					if item['attributes']['name'] == folderName:
						contents = self._getFolderContents(item['id'])
						break
		return contents

	def _getModel(self):
		"""
		Get the data of the requested model.

		Returns:
			dict: The data dict
		"""
		for item in self._getModelFolderContents():
			if item['attributes']['displayName'] == os.path.basename(self.path):
				return item

	def _getVersions(self):
		"""
		Get all versions of the requested model.

		Returns:
			dict: The versions dict
		"""
		url = 'https://developer.api.autodesk.com/data/v1/projects/{project}/items/{model}/versions'
		req = requests.get(
		    url.format(project=self.projectId,
		               model=self.modelId),
		    headers=self._authHeader
		)
		responseData = req.json()
		return responseData['data']

	@property
	def region(self):
		"""
		The region of the hub where the requested model is located.

		Returns:
			string: The region string
		"""
		url = 'https://developer.api.autodesk.com/project/v1/hubs/{}'.format(self.hubId)
		req = requests.get(url, headers=self._authHeader)
		responseData = req.json()
		items = responseData['data']
		return items['attributes']['region']

	@property
	def modelGuid(self):
		"""
		The model Guid of the requested model.

		Returns:
			string: The model Guid
		"""
		return System.Guid(
		    self.lastVersion['attributes']['extension']['data']['modelGuid']
		)

	@property
	def projectGuid(self):
		"""
		The project Guid of the requested model.

		Returns:
			string: The project Guid
		"""
		return System.Guid(
		    self.lastVersion['attributes']['extension']['data']['projectGuid']
		)

	def open(self, detach=False):
		"""
		Open the requested cloud based model.

		Args:
			detach (bool, optional): Detach from central. Defaults to False.

		Returns:
			object: A Revit document object
		"""
		import revitron
		options = revitron.DB.OpenOptions()
		modelPath = revitron.DB.ModelPathUtils.ConvertCloudGUIDsToCloudPath(
		    self.region,
		    self.projectGuid,
		    self.modelGuid
		)
		if detach:
			options.DetachFromCentralOption = revitron.DB.DetachFromCentralOption.DetachAndPreserveWorksets
		return HOST_APP.uiapp.OpenAndActivateDocument(modelPath, options, False)
