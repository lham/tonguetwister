from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class IndexedItem:
    def __init__(self, index=None, item=None):
        self.index = index
        self.item = item


class ListView(BoxLayout):
    selected_element = ObjectProperty(IndexedItem())

    def __init__(self, items, render_item=None, item_height=25, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self._list_items = []
        self._render_item = render_item
        self._item_height = item_height

        for item in items:
            self.add_list_item(item)

    def on_minimum_height(self, _, minimum_height):
        self.height = minimum_height

    def _create_list_item(self, index, item):
        list_item = ListViewItem(index, item, self._render_item, self, height=self._item_height, size_hint_y=None)
        list_item.bind(selected=self._on_list_item_selected)

        return list_item

    def _on_list_item_selected(self, instance, selected):
        prev_index = self.selected_element.index

        if selected:
            self.selected_element = IndexedItem(instance.index, instance.item)
            Clock.schedule_once(lambda _: self._rebuild_list_items(instance.index, prev_index), 0)

    def _rebuild_list_items(self, index, prev_index):
        if prev_index is not None:
            self._list_items[prev_index].rebuild()

        if index is not None:
            self._list_items[index].rebuild()

    def add_list_item(self, item):
        list_item = self._create_list_item(len(self._list_items), item)
        self._list_items.append(list_item)
        self.add_widget(list_item)

    def clear_list_items(self):
        self._list_items = []
        self.clear_widgets()
        self.selected_element = IndexedItem()

    def select_item(self, index):
        if self.selected_element.index is not None:
            previously_selected = self._list_items[self.selected_element.index]
            previously_selected.selected = False

        if len(self._list_items) > 0:
            self._list_items[index].selected = True


class ListViewItem(BoxLayout):
    selected = BooleanProperty(False)

    def __init__(self, index, item, render_function, parent, **kwargs):
        super().__init__(**kwargs)
        self.item = item
        self.index = index
        self._render = render_function
        self.add_widget(self._build_item(parent))

    def _build_item(self, parent):
        if self._render is None:
            return Label(text=self.item, halign='left', valign='middle', text_size=(parent.width, None))
        else:
            return self._render(self.index, self.item, parent)

    def rebuild(self):
        self.clear_widgets()
        self.add_widget(self._build_item(self.parent))

    def on_touch_down(self, touch):
        if self.parent.collide_point(*touch.pos):
            if self.collide_point(*touch.pos):
                self.selected = True
            else:
                self.selected = False
