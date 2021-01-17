from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout


class ActionBarPanel(BoxLayout):
    spacing = 10
    orientation = 'vertical'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action_bar = self.build_action_bar()
        self.add_widget(self.action_bar)

    @staticmethod
    def build_action_bar():
        action_bar = StackLayout(orientation='rl-tb', size_hint_y=None)
        action_bar.bind(minimum_height=action_bar.setter('height'))

        return action_bar

    def add_action_bar_widget(self, widget):
        self.action_bar.add_widget(widget)
