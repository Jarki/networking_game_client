from utility.clear_layout import clear_layout


class BasicForm:
    """abstract class for any form to inherit"""
    def __init__(self):
        self.wrapper = None

    def clear(self):
        clear_layout(self.wrapper, True)
