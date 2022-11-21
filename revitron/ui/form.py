"""
This submodule contains a collection of basic form elements.
"""
import System.Windows
from rpw.ui.forms import CheckBox as RPWCheckBox
from rpw.ui.forms import TextBox as RPWTextBox
from rpw.ui.forms import Label as RPWLabel
from rpw.ui.forms import ComboBox as RPWComboBox

MARGIN = System.Windows.Thickness(0, 0, 0, 10)


class CheckBox():
	"""
	A simple checkbox component.
	"""

	@staticmethod
	def create(window, containerName, key, input, title=None):
		"""
		A helper function that creates checkbox form element.

		Args:
			window (object): The parent window object
			containerName (string): The name of the parent container
			key (string): The key that references the value in the window values dictionary
			input (mixed): The input value
			title (string, optional): The checkbox title. Defaults to the key.
		"""
		import revitron
		if not title:
			title = key
		key = revitron.String.sanitize(key)
		if isinstance(input, dict):
			state = input.get(key)
		else:
			state = input
		if not state:
			state = False
		container = window.getContainer(containerName)
		container.Children.Add(
		    RPWCheckBox(
		        key,
		        title,
		        state,
		        Width=window.widthForm,
		        Margin=System.Windows.Thickness(0, 10, 0, 10)
		    )
		)


class Label():
	"""
	A simple label component.
	"""

	@staticmethod
	def create(window, containerName, text):
		"""
		A helper function that creates a label component.

		Args:
			window (object): The parent window object
			containerName (string): The name of the parent container
			text (string): The label text
		"""
		container = window.getContainer(containerName)
		container.Children.Add(RPWLabel(text))


class SelectBox():
	"""
	A dropdown field.
	"""

	@staticmethod
	def create(window, containerName, key, options, input, title=None):
		"""
		Create a select dropdown in a specific container of a given window.

		Args:
			window (Window): The Revitron Window object
			containerName (string): The name of the target container
			key (string): The key
			options (dict|list): The dict or list of options
			input (dict|string): The value for the field - a configuration dict where 'key' stores the value, or simply a string
			title (string, optional): An optional title. Defaults to None.
		"""
		import revitron
		if not title:
			title = key
		key = revitron.String.sanitize(key)
		if isinstance(input, dict):
			selected = input.get(key)
		else:
			selected = input
		if selected not in options:
			try:
				selected = sorted(options.keys())[0]
			except:
				selected = sorted(options)[0]
		container = window.getContainer(containerName)
		container.Children.Add(RPWLabel(title))
		container.Children.Add(
		    RPWComboBox(key, options, selected, Width=window.widthForm, Margin=MARGIN)
		)


class TextBox():
	"""
	A text input field
	"""

	@staticmethod
	def create(window, containerName, key, input, title=None, default=''):
		"""
		Create a text box in a specific container of a given window.

		Args:
			window (Window): The Revitron Window object
			containerName (string): The name of the target container
			key (string): The key
			input (dict|string): The value for the field - a configuration dict where 'key' stores the value, or simply a string
			title (string, optional): An optional title. Defaults to None.
		"""
		import revitron
		if not title:
			title = key
		key = revitron.String.sanitize(key)
		if isinstance(input, dict):
			value = input.get(key)
		else:
			value = input
		if default and not value:
			value = default
		container = window.getContainer(containerName)
		container.Children.Add(RPWLabel(title))
		container.Children.Add(
		    RPWTextBox(
		        key,
		        value,
		        Width=window.widthForm,
		        Height=28,
		        Padding=System.Windows.Thickness(4),
		        Margin=MARGIN
		    )
		)
