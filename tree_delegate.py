
from PyQt5 import QtCore, QtGui, QtWidgets


class TreeDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super(TreeDelegate, self).__init__()

    def createEditor(self, parent, option, index):
        """
        Returns the editor to be used for editing the data item with the given index

        :param parent: The editor's parent widget
        :type parent: QtWidgets.QWidget
        :param option: Used to describe the parameters used to draw an item in a view
        :type option: QtWidgets.QStyleOptionViewItem
        :param index: Item index in the model
        :type index: QtCore.QModelIndex
        :return: Editor Widget
        :rtype: QtWidgets.QWidget
        """
        editor = QtWidgets.QLineEdit(parent)
        editor.setFrame(False)
        return editor

    def setEditorData(self, editor, index):
        """
        This function copies the model data into the editor.

        :param editor: editor
        :type editor: QtWidgets.QWidget
        :param index: index
        :type index: QtCore.QModelIndex
        :return: None
        """
        value = index.model().data(index, QtCore.Qt.EditRole)
        if value.convert(QtCore.QMetaType.QString):
            editor.setText(value.value())

    def setModelData(self, editor, model, index):
        """
        When the user has finished editing the value in the editor (widget), the view asks the delegate to store the
        edited value in the model by calling this function.

        :param editor: editor
        :type editor: QtWidgets.QWidget
        :param model: model
        :type model: QtCore.QAbstractItemModel
        :param index: index
        :type index: QtCore.QModelIndex
        :return: None
        """
        value = editor.text()
        var = QtCore.QVariant(value)
        model.setData(index, var, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        """
        It is the responsibility of the delegate to manage the editor's geometry.
        The geometry must be set when the editor is created,
        and when the item's size or position in the view is changed.

        :param editor: editor
        :type editor: QtWidgets.QWidget
        :param option: Used to describe the parameters used to draw an item in a view
        :type option: QtWidgets.QStyleOptionViewItem
        :param index: Item index in the model
        :type index: QtCore.QModelIndex
        """
        editor.setGeometry(option.rect)
