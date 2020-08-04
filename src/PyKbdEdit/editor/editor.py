# This file is part of PyKbdEdit
#
# Copyright (C) 2020  Nulano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import dataclasses
import typing
from bisect import bisect_left
from typing import Union

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt5.QtWidgets import QComboBox, QFileDialog, QLineEdit, QMainWindow, QPushButton, QGroupBox

from PyKbd.layout import Layout, ScanCode, KeyCode

from .._util import connect, load_layout, connected
from . import _version
from .keyboardwidget import KeyboardWidget
from .metadata import MetadataWindow

__version__ = _version


class _ComboVscModel(QAbstractListModel):
    RoleVsc = Qt.UserRole
    RoleName = Qt.UserRole + 1
    RoleWinVk = Qt.UserRole + 2

    keys: list
    inserting: Union[bool, ScanCode]

    def __init__(self, parent, layout: Layout):
        super().__init__(parent)
        self.kbd_layout = layout
        self.reload()

    def reload(self):
        self.beginResetModel()
        self.keys = list(sorted(self.kbd_layout.keymap.keys()))
        self.inserting = False
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.keys) + (1 if self.inserting is not False else 0)

    def data(self, index: QModelIndex, role: int = ...):
        if not 0 <= index.row() < len(self.keys):
            return None
        vsc = self.keys[index.row()]
        keycode = self.kbd_layout.keymap[vsc]
        if role == Qt.DisplayRole:
            # TODO default VSC name database?
            return f"{vsc.to_string()} - {keycode.name or f'VK {keycode.win_vk}'}"
        elif role == Qt.EditRole:
            return vsc.to_string()
        elif role == _ComboVscModel.RoleVsc:
            return vsc
        elif role == _ComboVscModel.RoleName:
            # TODO default VSC name database?
            return keycode.name
        elif role == _ComboVscModel.RoleWinVk:
            return keycode.win_vk

    def setData(self, index: QModelIndex, value, role: int = ...) -> bool:
        if role == Qt.EditRole:
            assert self.inserting is True
            assert index.row() == len(self.keys)
            try:
                vsc = ScanCode.from_string(value)
                if vsc in self.kbd_layout.keymap:
                    raise ValueError("duplicate vsc")
                self.inserting = vsc
                return True
            except ValueError as exc:
                print(exc)
                self.inserting = False
                return False
        else:
            if not 0 <= index.row() < len(self.keys):
                return False
            vsc = self.keys[index.row()]
            keycode = self.kbd_layout.keymap[vsc]
            if role == _ComboVscModel.RoleName:
                self.kbd_layout.keymap[vsc] = dataclasses.replace(keycode, name=value)
            elif role == _ComboVscModel.RoleWinVk:
                self.kbd_layout.keymap[vsc] = dataclasses.replace(keycode, win_vk=value)
            else:
                return False
            self.dataChanged.emit(index, index)
            return True

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        assert row == len(self.keys)
        assert count == 1
        assert self.inserting is False
        self.inserting = True
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        assert self.inserting is False
        self.beginRemoveRows(parent, row, row + count)
        for i in range(row, row + count):
            del self.kbd_layout.keymap[self.keys[i]]
        self.keys = self.keys[:row] + self.keys[row + count:]
        self.endRemoveRows()
        return True


class _ComboVkModel(QAbstractListModel):
    values = [
        *range(256)
    ]

    def __init__(self, parent, layout):
        super(_ComboVkModel, self).__init__(parent)
        self.kbd_layout = layout

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.values)

    def data(self, index: QModelIndex, role: int = ...):
        if index.isValid():
            if role == Qt.UserRole:
                return self.values[index.row()]
            elif role == Qt.DisplayRole:
                return hex(self.values[index.row()])

    def match(self, start: QModelIndex, role: int, value, hits: int = ..., flags=...) -> typing.List[QModelIndex]:
        if role == Qt.DisplayRole:
            role = Qt.UserRole
            value = int(value, 16)
        if role == Qt.UserRole:
            i = bisect_left(self.values, value)
            if i != len(self.values) and self.values[i] == value:
                return [self.index(i, 0)]
            return []
        else:
            return super(_ComboVkModel, self).match(start, role, value, hits, flags)


class EditorWindow(QMainWindow):
    filename: typing.Optional[str]
    kbd_layout: Layout

    def __init__(self, layout: Union[str, Layout]):
        super(EditorWindow, self).__init__()

        if isinstance(layout, str):
            with open(layout, encoding="utf-8") as f:
                data = f.read()
            self.filename = layout
            layout = Layout.from_json(data)
        else:
            self.filename = None

        assert isinstance(layout, Layout)
        self.kbd_layout = layout

        load_layout(self, __name__)
        connect(self)

        self.load_metadata()
        self.setup_keymap()

    # ==================== BASE ====================

    def closeEvent(self, ev):
        print("closing...")
        ev.accept()

    def load_metadata(self):
        self.setWindowTitle(self.kbd_layout.name)

    @connected()
    def actionSave_(self):
        if not self.filename:
            self.action_save_as("Save Layout...")
        else:
            print("saved as", self.filename)

    @connected()
    def actionSaveAs_(self, caption="Save Layout As..."):
        filename = QFileDialog.getSaveFileName(
            self, caption, self.filename, "Layout Files (*.json);;All Files (*.*)"
        )[0]
        if filename:
            self.filename = filename
            self.action_save()

    @connected()
    def actionMetadata_(self):
        dlg = MetadataWindow(self, self.kbd_layout)
        dlg.accepted.connect(self.load_metadata)
        dlg.open()

    # ==================== KEYMAP ====================

    kbdKeymap: KeyboardWidget
    comboVsc: QComboBox
    btnVscRemove: QPushButton
    groupVsc: QGroupBox
    editVscName: QLineEdit
    comboVscVk: QComboBox

    def setup_keymap(self):
        self.comboVsc.setModel(_ComboVscModel(self.comboVsc, self.kbd_layout))
        self.comboVscVk.setModel(_ComboVkModel(self.comboVscVk, self.kbd_layout))
        # XXX for some reason this isn't firing on initial model set
        self.comboVsc_currentIndexChanged(self.comboVsc.currentIndex())

    @connected()
    def comboVsc_currentIndexChanged(self, i):
        print("comboVsc_currentIndexChanged:", i)
        model = self.comboVsc.model()

        if i < 0:
            self.btnVscRemove.setEnabled(False)
            self.groupVsc.setEnabled(False)
            return
        else:
            self.btnVscRemove.setEnabled(True)
            self.groupVsc.setEnabled(True)

        if i == len(model.keys):
            vsc = model.inserting
            assert isinstance(vsc, ScanCode)
            assert vsc not in self.kbd_layout.keymap
            self.kbd_layout.keymap[vsc] = KeyCode(0)
            model.reload()
            self.comboVsc.setCurrentIndex(model.keys.index(vsc))
        else:
            vsc = model.keys[i]
            keycode = self.kbd_layout.keymap[vsc]
            self.editVscName.setText(keycode.name)
            self.comboVscVk.setCurrentIndex(self.comboVscVk.findData(keycode.win_vk))

    @connected()
    def editVscName_editingFinished(self):
        self.comboVsc.setItemData(
            self.comboVsc.currentIndex(),
            self.editVscName.text(),
            _ComboVscModel.RoleName,
        )

    @connected()
    def comboVscVk_currentIndexChanged(self, i):
        self.comboVsc.setItemData(
            self.comboVsc.currentIndex(),
            self.comboVscVk.itemData(i),
            _ComboVscModel.RoleWinVk,
        )

    @connected()
    def btnVscRemove_(self):
        self.comboVsc.removeItem(self.comboVsc.currentIndex())
