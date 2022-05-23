"""
This submodule contains the ``TransmissionData`` class 
which allows for editing the paths of linked files without opening a model.  
"""
import re
import shutil
import os
import sys


class TransmissionData:
	""" 
	A transmission data wrapper.
	"""

	refs = dict()

	def __init__(self, hostPath):
		"""
		Inits a new TransmissionData instance.

		Args:
			hostPath (string): The path of the host model
		"""
		import revitron

		if revitron.Document.isOpen(hostPath):
			print('The host model must be closed to edit transmission data!')
			sys.exit()

		self.hostPath = revitron.DB.FilePath(hostPath)
		self.data = revitron.DB.TransmissionData.ReadTransmissionData(self.hostPath)

		for refId in self.data.GetAllExternalFileReferenceIds():
			self.refs[refId.IntegerValue] = revitron.ExternalReference(
			    self.data.GetLastSavedReferenceData(refId)
			)

	def listLinks(self):
		"""
		List all links in the host document.
		"""
		for _id in self.refs:
			ref = self.refs[_id]
			print(ref.path)

	def moveLinksOnDisk(self, source, target):
		"""
		Moves all external CAD and RVT links on disk and relinks them.

		Args:
			source (string): The source directory 
			target (string): The target directory
		"""
		import revitron

		source = re.sub(r'\\$', '', source) + os.sep
		source = '^' + re.escape(source)
		target = re.sub(r'\\$', '', target)
		target = re.sub(r'\\', os.sep, target)

		for _id in self.refs:

			refId = revitron.DB.ElementId(_id)
			ref = self.refs[_id]

			if str(ref.type) in ['RevitLink', 'CADLink']:

				if re.search(source, ref.path, re.IGNORECASE):
					newPath = target + os.sep + re.sub(
					    source, '', ref.path, re.IGNORECASE
					)
				else:
					newPath = target + os.sep + os.path.basename(ref.path)

				print(newPath)

				if newPath != ref.path:
					try:
						os.makedirs(os.path.dirname(newPath))
						print('Created {}'.format(os.path.dirname(newPath)))
					except:
						pass
					try:
						shutil.copyfile(ref.path, newPath)
					except:
						pass

					self.data.SetDesiredReferenceData(
					    refId,
					    revitron.DB.FilePath(newPath),
					    revitron.DB.PathType.Absolute,
					    True
					)

		self.write()

	def replaceInPath(self, search, replace):
		"""
		Search and replace in all link paths of the document. 

		Args:
			search (string): The search string
			replace (string): The replacement string
		"""
		import revitron

		for _id in self.refs:

			refId = revitron.DB.ElementId(_id)
			ref = self.refs[_id]
			newPath = ref.path.replace(search, replace)
			self.data.SetDesiredReferenceData(
			    refId, revitron.DB.FilePath(newPath), revitron.DB.PathType.Absolute, True
			)

		self.write()

	def write(self):
		"""
		Writes the TransmissionData back to the model.
		"""
		import revitron

		self.data.IsTransmitted = True
		revitron.DB.TransmissionData.WriteTransmissionData(self.hostPath, self.data)
