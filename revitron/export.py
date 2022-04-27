"""
The ``export`` submodule hosts all classes related to sheet export such as **DWG** and **PDF**.
For example sending the currently active sheet to a PDF printer in the network works as follows::

	exporter = revitron.PDFExporter(printerAddress, printerPath)
	exporter.printSheet(revitron.ACTIVE_VIEW, 
					   'A0', 
					   'Landscape', 
					   'C:/pdf', 
					   '{Sheet Number}-{Sheet Title}')
					   
Please check out the 
`export tool <https://github.com/revitron/revitron-ui/blob/master/Revitron.tab/Revitron.panel/Export.pulldown/Export%20Sheets%20as%20PDF.pushbutton/Export%20Sheets%20as%20PDF_script.py>`_ 
of the **Revitron UI** extension to learn how to export a selection of sheets 
with a felxible configuration stored in a document.
"""
#-*- coding: UTF-8 -*-
import os, shutil, time, sys, glob, re
from pyrevit import script
from System.Collections.Generic import List


class CSVExporter:
	"""
	Export a schedule as CSV named by a file naming template. 
	"""

	def __init__(self):
		"""
		Inits a new CSVExporter instance.
		"""
		pass

	def exportSchedule(
	    self,
	    schedule,
	    directory,
	    template=False,
	    delimiter=';',
	    hasTitle=False
	):
		"""
		Exports a schedule.

		Args:
			schedule (object): A Revit schedule
			directory (string): A custom output directory. Defaults to False.
			template (string, optional): A name template. Defaults to '{View Name}'.
			delimiter (string, optional): A csv delimiter. Defaults to ';'.
			hasTitle (bool, optional): Set True to export schedule title. Defaults to False.

		Returns:
			string: The path of the exported CSV. False on error.
		"""
		import revitron

		if revitron.Element(schedule).getClassName() != 'ViewSchedule':
			revitron.Log().warning('Element is not a schedule!')
			return False

		if not directory:
			revitron.Log().warning('No directory specified!')
			return False

		if not template:
			template = '{View Name}'

		name = revitron.ParameterTemplate(schedule, template).render() + '.csv'

		if not os.path.exists(directory):
			os.makedirs(directory)

		options = revitron.DB.ViewScheduleExportOptions()
		options.FieldDelimiter = delimiter
		options.Title = hasTitle
		options.TextQualifier = revitron.DB.ExportTextQualifier['None']

		schedule.Export(directory, name, options)

		file = os.path.join(directory, name)

		return file


class DWGExporter:
	"""
	Export sheets as DWG named by a file naming template. 
	"""

	def __init__(self, setupName):
		"""
		Inits a new DWGExporter instance.

		Args:
			setupName (string): The name of a stored export setup
		"""
		import revitron
		self.options = revitron.DB.DWGExportOptions().GetPredefinedOptions(
		    revitron.DOC,
		    setupName
		)

	def exportSheet(self, sheet, directory, unit, template=False):
		"""
		Exports a sheet.

		Args:
			sheet (object): A Revit sheet
			directory (string): The export directory
			unit (object): The `export unit <https://www.revitapidocs.com/2020/1d3eb4f4-81d2-10a6-3eab-4a9c20e39053.htm>`_
			template (string, optional): A name template. Defaults to '{Sheet Number}-{Sheet Name}'.

		Returns:
			string: The path of the exported PDF. False on error.
		"""
		import revitron

		if revitron.Element(sheet).getClassName() != 'ViewSheet':
			revitron.Log().warning('Element is not a sheet!')
			return False

		if not directory:
			revitron.Log().warning('There is no DWG export directory defined!')
			sys.exit()

		if not template:
			template = '{Sheet Number}-{Sheet Name}'

		fullPath = os.path.join(
		    directory,
		    revitron.ParameterTemplate(sheet,
		                               template).render() + '.dwg'
		)

		path = os.path.dirname(fullPath)
		file = os.path.basename(fullPath)

		if not os.path.exists(path):
			os.makedirs(path)

		db = revitron.DB
		self.options.MergedViews = True
		self.options.TargetUnit = unit

		success = revitron.DOC.Export(
		    path,
		    file,
		    List[db.ElementId]([sheet.Id]),
		    self.options
		)

		if success:
			return fullPath

		return False


class PDFExporter:
	"""
	Export sheets as PDF named by a file naming template. 
	"""

	def __init__(self, printer, output):
		"""
		Inits a new PDFExporter instance.

		Args:
			printer (string): The printer network adress
			output (string): The printer output directory 
		"""
		import revitron

		if not printer or not output:
			revitron.Log().warning('PDF exporter is not configured!')
			sys.exit()

		self.printer = printer
		self.output = output
		self.manager = revitron.DOC.PrintManager
		self.sizes = dict()

		if self.manager.PrinterName.lower() != self.printer.lower():
			print('Setting current printer to: ' + self.printer)
			print('Please submit your sheets to be exported again ...')
			self.manager.SelectNewPrintDriver(self.printer)
			self.manager.Apply()
			sys.exit()

		self.manager.PrintRange = revitron.DB.PrintRange.Select
		self.manager.PrintToFile = True
		self.manager.CombinedFile = False
		self.manager.Apply()

		for size in self.manager.PaperSizes:
			self.sizes[size.Name] = size

	def printSheet(
	    self,
	    sheet,
	    size,
	    orientation='Landscape',
	    colorMode='Color',
	    directory=False,
	    template=False
	):
		"""
		Prints a sheet.

		Args:
			sheet (object): A Revit sheet
			size (string): A size name like A0 or A4
			orientation (string, optional): The orientation, 'Landscape' or 'Portrait'. Defaults to 'Landscape'.
			colorMode (string, optional): The color setting for the printed sheets. Defaults to 'Color'.
			directory (string, optional): A custom output directory. Defaults to False.
			template (string, optional): A name template. Defaults to '{Sheet Number}-{Sheet Name}'.

		Returns:
			string: The path of the exported PDF. False on error.
		"""
		import revitron

		if revitron.Element(sheet).getClassName() != 'ViewSheet':
			revitron.Log().warning('Element is not a sheet!')
			return False

		if not colorMode:
			colorMode = 'Color'

		if not directory:
			directory = self.output

		if not template:
			template = '{Sheet Number}-{Sheet Name}'

		path = os.path.join(
		    directory,
		    revitron.ParameterTemplate(sheet,
		                               template).render() + '.pdf'
		)

		if not os.path.exists(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path))

		transaction = revitron.Transaction()

		viewSet = revitron.DB.ViewSet()
		viewSet.Insert(sheet)

		viewSheetSetting = self.manager.ViewSheetSetting
		viewSheetSetting.CurrentViewSheetSet.Views = viewSet
		viewSheetSetting.SaveAs("_temp_")

		self.manager.PrintSetup.SaveAs("_temp_")
		self.manager.Apply()

		orientation = getattr(revitron.DB.PageOrientationType, orientation)

		# Set current print page settings.
		printParameters = self.manager.PrintSetup.CurrentPrintSetting.PrintParameters
		printParameters.ZoomType = revitron.DB.ZoomType.Zoom
		printParameters.Zoom = 100
		printParameters.PaperPlacement = revitron.DB.PaperPlacementType.Center
		printParameters.PageOrientation = orientation
		printParameters.PaperSize = self.sizes[size]
		printParameters.RasterQuality = revitron.DB.RasterQualityType.High
		printParameters.ColorDepth = getattr(revitron.DB.ColorDepthType, colorMode)

		# Set in-session print settings.
		printParameters = self.manager.PrintSetup.InSession.PrintParameters
		printParameters.ZoomType = revitron.DB.ZoomType.Zoom
		printParameters.Zoom = 100
		printParameters.PaperPlacement = revitron.DB.PaperPlacementType.Center
		printParameters.PageOrientation = orientation
		printParameters.PaperSize = self.sizes[size]
		printParameters.RasterQuality = revitron.DB.RasterQualityType.High
		printParameters.ColorDepth = getattr(revitron.DB.ColorDepthType, colorMode)

		# Again save settings.
		try:
			self.manager.PrintSetup.Save()
		except:
			self.manager.PrintSetup.SaveAs("_temp2_")

		self.manager.Apply()
		self.manager.SubmitPrint(sheet)
		viewSheetSetting.Delete()

		transaction.rollback()

		# Move file form temp output to directory.
		timePassed = time.time()
		moved = False

		while (time.time() - timePassed) < 30 and not moved:
			time.sleep(0.5)
			tempFiles = glob.glob(self.tempOutputPattern(sheet))
			if tempFiles:
				tempFile = tempFiles[0]
				time.sleep(2)
				if os.access(tempFile, os.W_OK):
					try:
						shutil.move(tempFile, path)
						moved = True
					except:
						pass

		if moved:
			return path

		return False

	def tempOutputPattern(self, sheet):
		"""
		Create a glob pattern to identify a printed PDF in the system output directory to be able to 
		move it to its correct location and rename it according to the given template.
		
		Please note that the PDF network printer has to be configured to save PDFs following the below naming scheme::
		
			[Revit File] - Sheet - [Sheet Number] - [Sheet Name].pdf
		
		For example::
		
			Project1 - Sheet - A101 - Unnamed.pdf

		Args:
			sheet (object): A Revit sheet objetc

		Returns:
			string: The generated glob pattern
		"""
		import revitron

		nr = re.sub(r'[^a-zA-Z0-9]+', '*', revitron.Element(sheet).get('Sheet Number'))
		name = re.sub(r'[^a-zA-Z0-9]+', '*', revitron.Element(sheet).get('Sheet Name'))
		printToFileName = re.sub(
		    r'\.pdf$',
		    '',
		    os.path.basename(self.manager.PrintToFileName)
		)
		return '{}/{}*Sheet*{}*{}*.pdf'.format(self.output, printToFileName, nr, name)
