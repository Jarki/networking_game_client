from forms.basic_form import BasicForm

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt


class WaitingForm(BasicForm):
	def __init__(self, central_widget: QWidget):
		super().__init__()

		self.wrapper = QVBoxLayout()
		self.wrapper.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.waiting_label = QLabel('Waiting for the game to start...')

		self.wrapper.addWidget(self.waiting_label)
		central_widget.layout().addLayout(self.wrapper)

