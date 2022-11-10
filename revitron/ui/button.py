"""
A basic button module that integrates well into Revitron windows.
"""
import System.Windows
import System.Windows.Media
import System.Windows.Media.Colors
import System.Drawing
from rpw.ui.forms import Button as RPWButton


class Button(RPWButton):
	"""
	A simple Ok/Cancel button to be used in Revitron windows.
	"""

	def __init__(self, text, window, cancel=False, **kwargs):
		"""
		Initialize a new Button instance.

		Args:
			text (string): The button label text
			window (object): The parent window object
			cancel (bool, optional): If true, the window is closed without returning data. Defaults to False.
		"""
		self.set_attrs(**kwargs)
		self.Content = text
		self.window = window
		self.cancel = cancel

	def OnClick(self):
		"""
		The OnClick handler function.
		"""
		if self.cancel:
			self.window.close()
		else:
			self.window.ok = True
			self.window.getValues()

	@staticmethod
	def create(window, containerName, text, cancel=True):
		"""
		A helper to easily create a new button instance

		Args:
			window (object): The parent window object
			containerName (string): The name of the parent container
			text (strict): The button label text
			cancel (bool, optional): The cancel option for the button. Defaults to True.
		"""
		container = window.getContainer(containerName)
		if cancel:
			color = System.Windows.Media.Colors.SteelBlue
			bgColor = System.Windows.Media.Colors.GhostWhite
		else:
			color = System.Windows.Media.Colors.GhostWhite
			bgColor = System.Windows.Media.Colors.SteelBlue
		container.Children.Add(
		    Button(
		        text,
		        window,
		        cancel=cancel,
		        Width=120,
		        Height=30,
		        Margin=System.Windows.Thickness(10, 0, 0, 0),
		        Foreground=System.Windows.Media.SolidColorBrush(color),
		        Background=System.Windows.Media.SolidColorBrush(bgColor),
		        BorderBrush=System.Windows.Media.SolidColorBrush(
		            System.Windows.Media.Colors.SteelBlue
		        )
		    )
		)