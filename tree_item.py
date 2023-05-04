
from PyQt5.QtCore import QVariant


class TreeItem:
    """
    This is a basic class. It is used to hold column data and information about its position in the tree structure.
    """

    def __init__(self, data, parent=None):
        """
        :param data: column data
        :type data: list
        :param parent: parent item
        :type parent: TreeItem
        """
        self._childItems = []
        self._itemData = data
        self._parentItem = parent

    def append_child(self, child):
        """
        :param child: child item
        :type child: TreeItem
        :return: None
        """
        self._childItems.append(child)

    def child(self, row):
        """
        :param row: row
        :type row: int
        :return: child item
        :rtype: TreeItem
        """
        if (row < 0) or (row >= len(self._childItems)):
            return None
        return self._childItems[row]

    def child_count(self):
        """
        :return: number of children
        :rtype: int
        """
        return len(self._childItems)

    def column_count(self):
        """
        :return: number of columns
        :rtype: int
        """
        return len(self._itemData)

    def data(self, column):
        """
        :param column: column
        :type column: int
        :return: data
        :rtype: QVariant
        """
        if (column < 0) or (column >= len(self._itemData)):
            return QVariant()
        return self._itemData[column]

    def set_data(self, column, value):
        """
        :param column: column number
        :type column: int
        :param value: value to be stored
        :type value: QVariant
        :return: whether values were stored successfully
        :rtype: bool
        """
        if (column < 0) or (column >= len(self._itemData)):
            return False

        self._itemData[column] = value
        return True

    def insert_children(self, position, count, columns):
        """
        :param position: row number where children will be inserted
        :type position: int
        :param count: number of children to insert
        :type count: int
        :param columns: number of columns for each new child
        :type columns: int
        :return: whether children were successfully inserted
        :rtype: bool
        """
        if (position < 0) or (position > len(self._childItems)):
            return False

        for row in range(count):
            data = [''] * columns
            item = TreeItem(data, self)
            self._childItems.insert(position, item)

        return True

    def remove_children(self, position, count):
        """
        :param position: row number
        :type position: int
        :param count: number of children to remove
        :type count: int
        :return: whether children were removed successfully
        :rtype: bool
        """
        if (position < 0) or (position + count > len(self._childItems)):
            return False

        for row in range(count):
            self._childItems.pop(position)

        return True

    def insert_columns(self, position, columns):
        """
        :param position: column number
        :type position: int
        :param columns: number of columns
        :type columns: int
        :return: whether columns were inserted successfully
        :rtype: bool
        """
        if (position < 0) or (position > len(self._itemData)):
            return False

        for column in range(columns):
            self._itemData.insert(position, '')

        for child in self._childItems:
            child: TreeItem
            child.insert_columns(position, columns)

        return True

    def remove_columns(self, position, columns):
        """
        :param position: column number
        :type position: int
        :param columns: number of columns to remove
        :type columns: int
        :return: whether columns were removed successfully
        :rtype: bool
        """
        if (position < 0) or (position + columns > len(self._itemData)):
            return False

        for column in range(columns):
            self._itemData.pop(position)

        for child in self._childItems:
            child: TreeItem
            child.remove_columns(position, columns)

        return True

    def child_number(self):
        """
        :return: row
        :rtype: int
        """
        if self._parentItem:
            return self._parentItem._childItems.index(self)

        return 0

    def parent_item(self):
        """
        :return: parent item
        :rtype: TreeItem
        """
        return self._parentItem
