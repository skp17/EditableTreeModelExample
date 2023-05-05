
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from tree_delegate import TreeDelegate
from tree_model import TreeModel

BUNDLE = True
###########################
if BUNDLE is True:
    from ui_main_window import Ui_MainWindow
else:
    qtCreatorFileMainW = r"./main_window.ui"
    Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFileMainW)
##########################


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.resize(600, 700)
        self.setWindowTitle('Editable Tree Model')
        self.view.setAlternatingRowColors(True)

        headers = ["Title", "Description"]

        file = QtCore.QFile(r'.\default.txt')
        file.open(QtCore.QIODevice.ReadOnly | QtCore.QFile.Text)
        data = QtCore.QTextStream(file).readAll()
        model = TreeModel(headers, data, self)
        file.close()

        self.view.setItemDelegate(TreeDelegate())

        self.view.setModel(model)
        for column in range(model.columnCount()):
            self.view.resizeColumnToContents(column)

        # Connect signals
        self.exitAction.triggered.connect(self.close)
        self.view.selectionModel().selectionChanged.connect(self.update_actions)
        self.actionsMenu.aboutToShow.connect(self.update_actions)
        self.insertRowAction.triggered.connect(self._insert_row)
        self.insertColumnAction.triggered.connect(self._insert_column)
        self.removeRowAction.triggered.connect(self._remove_row)
        self.removeColumnAction.triggered.connect(self._remove_column)
        self.insertChildAction.triggered.connect(self._insert_child)

        self.update_actions()
        self.view.expandAll()

    def _insert_child(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()

        if model.columnCount(index) == 0:
            if not model.insertColumn(0, index):
                return

        if not model.insertRow(0, index):
            return

        for column in range(model.columnCount()):
            child = model.index(0, column, index)
            model.setData(child, QtCore.QVariant('[No data]'), QtCore.Qt.EditRole)
            if not model.headerData(column, QtCore.Qt.Horizontal).isValid():
                model.setHeaderData(column, QtCore.Qt.Horizontal, QtCore.QVariant('[No header]'), QtCore.Qt.EditRole)

        self.view.selectionModel().setCurrentIndex(model.index(0, 0, index), QtCore.QItemSelectionModel.ClearAndSelect)

        self.update_actions()

    def _insert_column(self):
        model = self.view.model()
        column = self.view.selectionModel().currentIndex().column()

        # Insert a column in the parent item.
        changed = model.insertColumn(column + 1)
        if changed:
            model.setHeaderData(column + 1, QtCore.Qt.Horizontal, QtCore.QVariant('[No header]'), QtCore.Qt.EditRole)

        self.update_actions()

        return changed

    def _insert_row(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()

        if not model.insertRow(index.row() + 1, index.parent()):
            return

        self.update_actions()

        for column in range(model.columnCount(index.parent())):
            child = model.index(index.row() + 1, column, index.parent())
            model.setData(child, QtCore.QVariant('[No data]'), QtCore.Qt.EditRole)

    def _remove_column(self):
        model = self.view.model()
        column = self.view.selectionModel().currentIndex().column()

        # Remove columns in each child of the parent item.
        changed = model.removeColumn(column)
        if changed:
            self.update_actions()

        return changed

    def _remove_row(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()
        if model.removeRow(index.row(), index.parent()):
            self.update_actions()

    def update_actions(self):
        has_selection = not self.view.selectionModel().selection().isEmpty()
        self.removeRowAction.setEnabled(has_selection)
        self.removeColumnAction.setEnabled(has_selection)

        has_current = self.view.selectionModel().currentIndex().isValid()
        self.insertRowAction.setEnabled(has_current)
        self.insertColumnAction.setEnabled(has_current)

        if has_current:
            self.view.closePersistentEditor(self.view.selectionModel().currentIndex())

            row = self.view.selectionModel().currentIndex().row()
            column = self.view.selectionModel().currentIndex().column()
            if self.view.selectionModel().currentIndex().parent().isValid():
                self.statusbar.showMessage(f'Position: ({row},{column})')
            else:
                self.statusbar.showMessage(f'Position: ({row},{column} in top level)')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
