"""
The ``window`` submodule contains classes for generating UI windows.
"""
from abc import ABCMeta, abstractmethod
from rpw.ui.forms import FlexForm
from rpw.ui.forms.resources import *


class AbstractWindow(FlexForm):
	"""
	An abstract base window class.
	"""

	__metaclass__ = ABCMeta

	width = None
	height = None
	ok = False
	values = {}
	layout = ''

	def __init__(self, title, width=520, height=620, **kwargs):
		"""
		Init a new window object.

		Args:
			title (string): The window title
			width (int, optional): The window width. Defaults to 520.
			height (int, optional): The window height. Defaults to 620.
		"""
		self.width = width
		self.height = height
		self.ui = wpf.LoadComponent(self, StringReader(self._renderLayout()))
		self.ui.Title = title
		for key, value in kwargs.iteritems():
			setattr(self, key, value)

	def getContainer(self, name):
		"""
		Get the container within the window by name.

		Args:
			name (name): The container name

		Returns:
			object: The container in the window
		"""
		import revitron
		return getattr(self, revitron.String.sanitize(name))

	def close(self):
		"""
		Close the window
		"""
		self.DialogResult = True
		self.Close()

	@abstractmethod
	def _renderLayout(self):
		pass

	@abstractmethod
	def getValues(self):
		pass


class TabWindow(AbstractWindow):
	"""
	A window where the content is split into multiple custom tabs.
	"""

	layout = """
		<Window
			xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
			xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
			xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
			xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
			xmlns:local="clr-namespace:WpfApplication1" mc:Ignorable="d"
			Height="{height}" Width="{width}"
			WindowStartupLocation="CenterScreen"
			Topmost="True"
			>
			<StackPanel Name="MainGrid" Margin="0,10,0,10">
				<TabControl Name="Tabs" TabStripPlacement="Top" Margin="10,10,10,10">
					{tabs}
				</TabControl>
				<StackPanel HorizontalAlignment="Right" Orientation="Horizontal" Name="Buttons" Margin="10,10,10,0"></StackPanel>
			</StackPanel>
		</Window>
		"""

	def __init__(
	    self,
	    title,
	    tabs,
	    width=520,
	    height=620,
	    cancelButtonText='Cancel',
	    okButtonText='OK',
	    **kwargs
	):
		"""
		Init a new tabbed window.

		Args:
			title (_type_): _description_
			tabs (_type_): _description_
			width (int, optional): _description_. Defaults to 520.
			height (int, optional): _description_. Defaults to 620.
			cancelButtonText (str, optional): _description_. Defaults to 'Cancel'.
			okButtonText (str, optional): _description_. Defaults to 'OK'.
		"""
		from revitron.ui import Button
		self.tabs = tabs
		AbstractWindow.__init__(self, title, width=width, height=height, **kwargs)
		Button.create(self, 'Buttons', cancelButtonText, True)
		Button.create(self, 'Buttons', okButtonText, False)

	def _renderLayout(self):
		import revitron
		renderedTabs = ''
		tabHeight = self.height - 170
		for tab in self.tabs:
			renderedTabs += """
				<TabItem Header="{header}">
					<StackPanel Name="{tab}" Height="{tabHeight}" Margin="5,10,5,5"></StackPanel>
				</TabItem>
			""".format(header=tab, tab=revitron.String.sanitize(tab), tabHeight=tabHeight)
		return self.layout.format(tabs=renderedTabs, width=self.width, height=self.height)

	def getValues(self):
		"""
		Get the values of all form elements in the window and store them in the ``values`` dictionary.
		"""
		import revitron
		containers = []
		values = {}
		for tab in self.tabs:
			containers.append(self.getContainer(revitron.String.sanitize(tab)))
		for container in containers:
			for component in container.Children:
				try:
					values[component.Name] = component.value
				except AttributeError:
					pass
		self.values = values
		self.close()
