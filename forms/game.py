from forms.basic_form import BasicForm
from game.board import Board


from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QPushButton, QWidget, QLayout
from PyQt5.QtCore import Qt


class Game(BasicForm):
    def __init__(self, container_layout: QLayout, container_widget: QWidget):
        super().__init__()

        self.wrapper = QGridLayout()
        self.wrapper.setSpacing(0)
        self.wrapper.setAlignment(Qt.AlignmentFlag.AlignAbsolute)

        def hello(button):
            button.sender().setStyleSheet('background:#000')

        Board(10).draw(self.wrapper)
        # cutout_num = 0
        #
        # # works somehow
        # for i in range(21):
        #     if i < 11:
        #         if not i % 2:
        #             cutout_num = i + 2
        #
        #     if i >= 11:
        #         if i % 2:
        #             cutout_num = i - 2 * abs(20 / 2 - i) + 1
        #
        #     for j in range(21):
        #         button = QPushButton('')
        #
        #         if not i % 2:
        #             if not j % 2:
        #                 button.setMaximumWidth(8)
        #                 button.setMaximumHeight(8)
        #                 button.setEnabled(False)
        #             else:
        #                 button.setMaximumWidth(42)
        #                 button.setMaximumHeight(8)
        #                 # button.setText(f'{cutout_num}')
        #         else:
        #             if not j % 2:
        #                 button.setMaximumWidth(8)
        #                 button.setMaximumHeight(42)
        #             else:
        #                 # button.setText(f'{cutout_num}')
        #                 button.setMaximumSize(42, 42)
        #                 button.setEnabled(False)
        #
        #         if abs((20 / 2) - j) - cutout_num >= 1:
        #             button.setVisible(False)
        #
        #         button.clicked.connect(lambda: hello(button))
        #         self.wrapper.addWidget(button, i, j)


        # for i in range(20):
        #     for j in range(10):
        #         button = QPushButton(f'')
        #
        #         if j % 2 == 0:
        #             button.setMaximumWidth(8)
        #             button.setMinimumHeight(42)
        #         else:
        #             button.setMaximumHeight(8)
        #             button.setMaximumWidth(50)
        #
        #         button.clicked.connect(hello)
        #
        #         button.setStyleSheet("background:#fff;border:1px solid #000")
        #         self.wrapper.addWidget(button, i, j)
        #
        #     if i % 2:
        #         button = QPushButton(f'')
        #         button.setMaximumWidth(8)
        #         button.setMinimumHeight(42)
        #         button.setStyleSheet("background:#f00;border:1px solid #000; margin-left:-1px")
        #         self.wrapper.addWidget(button, i, 11)

        container_layout.addLayout(self.wrapper)

