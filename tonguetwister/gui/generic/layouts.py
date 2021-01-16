from kivy.uix.gridlayout import GridLayout

from tonguetwister.gui.generic.props import FixedHeight


class VerticalStackLayout(FixedHeight, GridLayout):
    cols = 1

    def __init__(self, spacing=(0, 0), **kwargs):
        super().__init__(spacing=spacing, **kwargs)
