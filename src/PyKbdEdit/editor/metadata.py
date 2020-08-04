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

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QMessageBox

from PyKbd.layout import Layout

from .._util import load_layout
from . import _version

__version__ = _version


class MetadataWindow(QDialog):
    def __init__(self, parent, layout: Layout):
        super(MetadataWindow, self).__init__(parent)

        self.kbd_layout = layout

        load_layout(self, __name__)

        self.load()
        self.editDllName.setValidator(
            QRegExpValidator(QRegExp("[a-zA-Z0-9_]{1,8}"))
        )
        self.accepted.connect(self.save)
        self.buttonBox.accepted.connect(lambda: self.check() and self.accept())

    def load(self):
        self.editName.setText(self.kbd_layout.name)
        self.editAuthor.setText(self.kbd_layout.author)
        self.editCopyright.setText(self.kbd_layout.copyright)
        self.spinVersionMajor.setValue(self.kbd_layout.version[0])
        self.spinVersionMinor.setValue(self.kbd_layout.version[1])
        self.editDllName.setText(self.kbd_layout.dll_name[:-4])

    def save(self):
        self.kbd_layout.name = self.editName.text()
        self.kbd_layout.author = self.editAuthor.text()
        self.kbd_layout.copyright = self.editCopyright.text()
        self.kbd_layout.version = (
            self.spinVersionMajor.value(), self.spinVersionMinor.value()
        )
        self.kbd_layout.dll_name = self.editDllName.text() + ".dll"

    def check(self):
        if not self.editDllName.hasAcceptableInput():
            QMessageBox.warning(
                self,
                "Invalid DLL Name",
                "You must enter a valid DLL name.",
                QMessageBox.Ok,
            )
            return False

        dllname = self.editDllName.text()
        if not dllname.startswith("kbd") or len(dllname) < 4:
            return QMessageBox.warning(
                self,
                "Invalid DLL Name",
                "It is strongly recommended to use a DLL name that starts with 'kbd'.\n"
                f"Are you sure you wish to use the DLL name '{dllname}.dll'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            ) == QMessageBox.Yes
