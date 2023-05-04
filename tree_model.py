
from PyQt5 import QtCore, QtGui, QtWidgets

from tree_item import TreeItem


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, headers: list, data: str, parent: QtCore.QObject = None):
        super(TreeModel, self).__init__(parent)

        self._rootItem = TreeItem(headers)
        self._setup_model_data(data.split('\n'), self._rootItem)

    def _get_item(self, index: QtCore.QModelIndex) -> TreeItem:
        """
        Since the model's interface to the other model/view components is based on model indexes,
        and since the internal data structure is item-based, many of the functions implemented by the model need
        to be able to convert any given model index to its corresponding item. For convenience and consistency,
        we have defined a getItem() function to perform this repetitive task
        """
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self._rootItem

    def data(self, index: QtCore.QModelIndex, role: int = ...) -> QtCore.QVariant:
        if not index.isValid():
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            item = self._get_item(index)
            return item.data(index.column())

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if not index.isValid():
            return QtCore.Qt.ItemFlags(QtCore.Qt.NoItemFlags)

        return QtCore.Qt.ItemIsEditable | QtCore.QAbstractItemModel.flags(self, index)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> QtCore.QVariant:
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._rootItem.data(section)

        return QtCore.QVariant()

    def index(self, row: int, column: int, parent: QtCore.QModelIndex = ...) -> QtCore.QModelIndex:
        if parent.isValid() and parent.column() != 0:
            return QtCore.QModelIndex()

        parent_item = self._get_item(parent)
        if not parent_item:
            return QtCore.QModelIndex()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex) -> QtCore.QModelIndex:
        if not index.isValid():
            return QtCore.QModelIndex()

        child_item = self._get_item(index)
        parent_item = child_item.parent_item() if child_item else None

        if parent_item == self._rootItem or not parent_item:
            return QtCore.QModelIndex()

        return self.createIndex(parent_item.child_number(), 0, parent_item)

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        if parent.isValid() and parent.column() > 0:
            return 0

        parent_item = self._get_item(parent)

        return parent_item.child_count() if parent_item else 0

    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return self._rootItem.column_count()

    def setData(self, index: QtCore.QModelIndex, value: QtCore.QVariant, role: int = ...) -> bool:
        if role == QtCore.Qt.EditRole:
            item = self._get_item(index)
            result = item.set_data(index.column(), value)

            if result:
                self.dataChanged.emit(index, index, [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole])
            return result

        return False  # todo: verify

    def setHeaderData(self, section: int, orientation: QtCore.Qt.Orientation, value: QtCore.QVariant, role: int = ...) -> bool:
        if role == QtCore.Qt.EditRole:
            if orientation == QtCore.Qt.Horizontal:
                result = self._rootItem.set_data(section, value)

                if result:
                    self.headerDataChanged.emit(orientation, section, section)
                return result

        return False  # todo: verify

    def insertRows(self, position: int, rows: int, parent: QtCore.QModelIndex = ...) -> bool:
        parent_item = self._get_item(parent)
        if not parent_item:
            return False

        self.beginInsertRows(parent, position, position + rows - 1)
        success = parent_item.insert_children(position, rows, self._rootItem.column_count())
        self.endInsertRows()

        return success

    def removeRows(self, position: int, rows: int, parent: QtCore.QModelIndex = ...) -> bool:
        parent_item = self._get_item(parent)
        if not parent_item:
            return False

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parent_item.remove_children(position, rows)
        self.endRemoveRows()

        return success

    def insertColumns(self, position: int, columns: int, parent: QtCore.QModelIndex = ...) -> bool:
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self._rootItem.insert_columns(position, columns)
        self.endInsertColumns()

        return success

    def removeColumns(self, position: int, columns: int, parent: QtCore.QModelIndex = ...) -> bool:
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self._rootItem.remove_columns(position, columns)
        self.endRemoveColumns()

        return success

    def _setup_model_data(self, lines: [], parent: TreeItem):
        parents = []
        indentations = []
        parents.append(parent)
        indentations.append(0)

        number = 0

        while number < len(lines):
            position = 0
            while position < len(lines[number]):
                if lines[number][position] != ' ':
                    break
                position += 1

            line_data = lines[number][position:].strip()

            if line_data:
                # Read the column data from the rest of the line.
                column_data = [string for string in line_data.split('\t') if string != '']

                if position > indentations[-1]:
                    # The last child of the current parent is now the new parent
                    # unless the current parent has no children.
                    parents[-1]: TreeItem
                    if parents[-1].child_count() > 0:
                        parents.append(
                            parents[-1].child(parents[-1].child_count() - 1)
                        )
                        indentations.append(position)
                else:
                    while (position < indentations[-1]) and (len(parents) > 0):
                        parents.pop()
                        indentations.pop()

                # Append a new item to the current parent's list of children.
                last_parent: TreeItem = parents[-1]
                last_parent.insert_children(last_parent.child_count(), 1, self._rootItem.column_count())
                for column in range(len(column_data)):
                    last_parent.child(last_parent.child_count() - 1).set_data(column, column_data[column])

            number += 1
