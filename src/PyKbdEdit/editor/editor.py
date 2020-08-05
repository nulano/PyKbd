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
from PyQt5.QtWidgets import (
    QAction,
    QComboBox,
    QFileDialog,
    QGroupBox,
    QLineEdit,
    QMainWindow,
    QMenu,
    QPushButton, QActionGroup,
)

from PyKbd.data import win_vk
from PyKbd.layout import KeyCode, Layout, ScanCode, ShiftState
from PyKbd.visualizer import all as all_keyboards

from .._util import connect, connected, load_layout
from . import _version
from .keyboardwidget import KeyboardWidget
from .metadata import MetadataWindow

__version__ = _version


class _ComboVscModel(QAbstractListModel):
    RoleVsc = Qt.UserRole
    RoleName = Qt.UserRole + 1
    RoleWinVk = Qt.UserRole + 2
    RoleNameComputed = Qt.UserRole + 3

    keys: list
    inserting: Union[bool, ScanCode]

    def __init__(self, parent, layout: Layout):
        super().__init__(parent)
        self.kbd_layout = layout
        self.reload()

    def reload(self):
        self.beginResetModel()
        self.kbd_layout.keymap = {
            vsc: vk for vsc, vk in sorted(self.kbd_layout.keymap.items())
            if vsc == self.inserting or not win_vk.code_to_vk.get(vk.win_vk & ~win_vk.KBDEXT, win_vk.VK__none_).reserved
        }
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
            vk = win_vk.code_to_vk.get(keycode.win_vk & ~win_vk.KBDEXT)
            name = keycode.name or self.data(index, _ComboVscModel.RoleNameComputed)
            if vk:
                name = f"{name} ({str(vk)})"
            return f"{vsc.to_string()} - {name}"
        elif role == Qt.EditRole:
            return vsc.to_string()
        elif role == _ComboVscModel.RoleVsc:
            return vsc
        elif role == _ComboVscModel.RoleName:
            return keycode.name
        elif role == _ComboVscModel.RoleWinVk:
            return keycode.win_vk
        elif role == _ComboVscModel.RoleNameComputed:
            name = "unnamed"
            vk = win_vk.translate(keycode.win_vk)
            if vk in self.kbd_layout.charmap:
                char = self.kbd_layout.charmap[vk].get(ShiftState(), None)
                if char:
                    name = f"'{char.char}'"
            return name

    def setData(self, index: QModelIndex, value, role: int = ...) -> bool:
        if role in (Qt.EditRole, Qt.DisplayRole):
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
                if isinstance(value, str):
                    value = value.strip()
                if value == "":
                    value = None
                self.kbd_layout.keymap[vsc] = dataclasses.replace(keycode, name=value)
            elif role == _ComboVscModel.RoleWinVk:
                if value is None:
                    return False
                self.kbd_layout.keymap[vsc] = dataclasses.replace(keycode, win_vk=value)
            else:
                return False
            self.dataChanged.emit(index, index)
            return True

    def match(self, start: QModelIndex, role: int, value: typing.Any, hits: int = ..., flags: typing.Union[Qt.MatchFlags, Qt.MatchFlag] = ...) -> typing.List[QModelIndex]:
        try:
            vsc = ScanCode.from_string(value)
            i = bisect_left(self.keys, vsc)
            if i < len(self.keys) and vsc == self.keys[i]:
                return [self.index(i, 0)]
        except ValueError:
            pass
        return super(_ComboVscModel, self).match(start, role, value, hits, flags)

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
    def __init__(self, parent, layout):
        super(_ComboVkModel, self).__init__(parent)
        self.kbd_layout = layout

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(win_vk.valid)

    def data(self, index: QModelIndex, role: int = ...):
        if index.isValid():
            if role == Qt.UserRole:
                return win_vk.valid[index.row()].code
            elif role == Qt.DisplayRole:
                vk = win_vk.valid[index.row()]
                assert isinstance(vk, win_vk.Vk)
                comment = f" - {vk.comment}" if vk.comment else ""
                return f"0x{vk.code:02X} - {str(vk)}{comment}"

    def match(self, start: QModelIndex, role: int, value, hits: int = ..., flags=...) -> typing.List[QModelIndex]:
        if role == Qt.DisplayRole:
            parts = value.split(" - ")
            name = parts[1]
            name = name[1:] if name[:1] == "*" else name
            vk = win_vk.name_to_vk.get(name, None)
            if not vk or vk.reserved:
                return []
            i = bisect_left(win_vk.valid, vk)
            if i < len(win_vk.valid) and win_vk.valid[i] == vk:
                return [self.index(win_vk.valid.index(vk), 0)]
        elif role == Qt.UserRole:
            vk = win_vk.code_to_vk.get(value & ~win_vk.KBDEXT)
            if not vk or vk.reserved:
                return []
            i = bisect_left(win_vk.valid, vk)
            if i < len(win_vk.valid) and win_vk.valid[i] == vk:
                return [self.index(win_vk.valid.index(vk), 0)]
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

        self.setup_base()
        self.setup_keymap()

    # ==================== BASE ====================

    menuKeyboard: QMenu
    actionKeyboardGroup: QActionGroup

    def setup_base(self):
        self.load_metadata()
        self.actionKeyboardGroup = QActionGroup(self)
        self.actionKeyboardGroup.triggered.connect(self.actionKeyboardGroup_)
        action = self.actionKeyboardGroup.addAction("Hidden")
        action.setData(None)
        action.setCheckable(True)
        for keyboard in all_keyboards:
            action = self.actionKeyboardGroup.addAction(keyboard.name)
            action.setData(keyboard)
            action.setCheckable(True)
        self.menuKeyboard.addActions(self.actionKeyboardGroup.actions())
        self.actionKeyboardGroup.actions()[1].trigger()

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

    def actionKeyboardGroup_(self, action):
        self.kbdKeymap.keyboard = action.data()

    # ==================== KEYMAP ====================

    kbdKeymap: KeyboardWidget
    comboVsc: QComboBox
    btnVscRemove: QPushButton
    groupVsc: QGroupBox
    editVscName: QLineEdit
    comboVscVk: QComboBox
    previous_vsc = None

    def setup_keymap(self):
        self.kbdKeymap.style = self.kbdKeymap_style
        self.kbdKeymap.clicked = self.kbdKeymap_clicked
        self.comboVsc.setModel(_ComboVscModel(self.comboVsc, self.kbd_layout))
        self.comboVscVk.setModel(_ComboVkModel(self.comboVscVk, self.kbd_layout))
        # XXX for some reason this isn't firing on initial model set
        self.comboVsc_currentIndexChanged(self.comboVsc.currentIndex())

    def kbdKeymap_style(self, scancode):
        if scancode not in self.kbd_layout.keymap:
            name, color, border = "", "#f88", "#a66"  # red
        else:
            keycode = self.kbd_layout.keymap[scancode]
            vk = win_vk.code_to_vk.get(keycode.win_vk & ~win_vk.KBDEXT)
            if not vk or vk.reserved:
                name, color, border = "", "#f88", "#a66"  # red
            else:
                name = keycode.name
                color, border = "#88f", "#66a"  # blue
                if not name:
                    color, border = "#8ff", "#6aa"  # cyan
                    vk = win_vk.translate(keycode.win_vk)
                    if vk in self.kbd_layout.charmap:
                        char = self.kbd_layout.charmap[vk].get(ShiftState(), None)
                        if char:
                            name = char.char
                if not name:
                    name = win_vk.code_to_vk[keycode.win_vk].name
                    color, border = "#f8f", "#a6a"  # magenta
        selected = self.comboVsc.currentData(_ComboVscModel.RoleVsc) == scancode
        return name, color, border, selected

    def kbdKeymap_clicked(self, scancode):
        if scancode not in self.kbd_layout.keymap:
            self.comboVsc.insertItem(len(self.kbd_layout.keymap), scancode.to_string())
            # select inserted entry to reload model
            self.comboVsc.setCurrentIndex(len(self.kbd_layout.keymap))
        # extra select if inserting to make sure it is selected
        self.comboVsc.setCurrentIndex(
            self.comboVsc.findText(scancode.to_string())
        )

    @connected()
    def comboVsc_currentIndexChanged(self, i):
        model = self.comboVsc.model()
        if i == len(model.keys):
            vsc = model.inserting
            assert isinstance(vsc, ScanCode)
            assert vsc not in self.kbd_layout.keymap
            self.kbd_layout.keymap[vsc] = KeyCode(0xFF)
            model.reload()
            self.comboVsc.setCurrentIndex(
                self.comboVsc.findText(vsc.to_string())
            )
        else:
            self.load_vsc(i)

    def load_vsc(self, i=None):
        if i is None:
            i = self.comboVsc.currentIndex()
        vsc = self.comboVsc.itemData(i, _ComboVscModel.RoleVsc)
        self.kbdKeymap.update_keys(self.previous_vsc)
        if vsc != self.previous_vsc:
            self.kbdKeymap.update_keys(vsc)
            self.previous_vsc = vsc
        if i < 0:
            self.btnVscRemove.setEnabled(False)
            self.groupVsc.setEnabled(False)
        else:
            self.btnVscRemove.setEnabled(True)
            self.groupVsc.setEnabled(True)
            keycode = self.kbd_layout.keymap[vsc]
            self.editVscName.setText(keycode.name)
            self.editVscName.setPlaceholderText(
                self.comboVsc.itemData(i, _ComboVscModel.RoleNameComputed)
            )
            self.comboVscVk.setCurrentIndex(self.comboVscVk.findData(keycode.win_vk))

    @connected()
    def editVscName_editingFinished(self):
        self.comboVsc.setItemData(
            self.comboVsc.currentIndex(),
            self.editVscName.text(),
            _ComboVscModel.RoleName,
        )
        self.load_vsc()

    @connected()
    def comboVscVk_currentIndexChanged(self, i):
        self.comboVsc.setItemData(
            self.comboVsc.currentIndex(),
            self.comboVscVk.itemData(i),
            _ComboVscModel.RoleWinVk,
        )
        self.load_vsc()

    @connected()
    def btnVscRemove_(self):
        self.comboVsc.removeItem(self.comboVsc.currentIndex())
