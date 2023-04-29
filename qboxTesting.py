
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QHBoxLayout, QMenu, QAbstractItemView
from PyQt6.QtCore import Qt
class MyListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAlternatingRowColors(True)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.itemDoubleClicked.connect(self.item_double_clicked)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        remove_action = menu.addAction("Remove")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == remove_action:
            self.remove_selected_items()

    def item_double_clicked(self, item):
        print(f"Item {item.text()} was double-clicked")

    def remove_selected_items(self):
        for item in self.selectedItems():
            self.takeItem(self.row(item))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.list_widget = MyListWidget()
        self.list_widget.addItem("Item 1")
        self.list_widget.addItem("Item 2")
        self.list_widget.addItem("Item 3")

        layout = QHBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
