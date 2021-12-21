from forms.basic_form import BasicForm

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import Qt


class SizeChooserForm(BasicForm):
	def __init__(self, central_widget: QWidget):
		super().__init__()

		self.wrapper = QVBoxLayout()
		self.wrapper.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.board_size_label = QLabel('Enter board radius (1-10)')
		self.board_size_input = QLineEdit()
		self.board_size_input.setMaximumWidth(256)
		self.board_size_button = QPushButton('Submit')

		self.wrapper.addWidget(self.board_size_label)
		self.wrapper.addWidget(self.board_size_input)
		self.wrapper.addWidget(self.board_size_button)

		central_widget.layout().addLayout(self.wrapper)

		self.callback = lambda x: x

	def set_button_handler(self, callback):
		self.board_size_button.clicked.connect(callback)

	def get_radius(self):
		return self.board_size_input.text()
