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

import string
from importlib.resources import open_text

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QFileDialog

from . import _version
from .editor import open_editor


__version__ = _version


class Launcher(QMainWindow):
    def __init__(self):
        super(Launcher, self).__init__()

        with open_text(__package__, __name__.rpartition('.')[2]+".ui") as layout:
            uic.loadUi(layout, self)

        for name, func in Launcher.__dict__.items():
            if name[:7] == "action_":
                action = getattr(
                    self, "action" + string.capwords(name[7:], sep="_").replace("_", "")
                )
                assert isinstance(action, QAction)
                action.triggered.connect(func.__get__(self, Launcher))

    def action_new(self, checked=False):
        from PyKbd.layout import Layout
        open_editor(Layout("Unnamed Layout"))

    def action_open(self, checked=False):
        filename = QFileDialog.getOpenFileName(
            self, "Open layout file", filter="Layout files (*.json);;All files (*.*)"
        )[0]
        if filename:
            open_editor(filename)

    def action_decompile(self, checked=False):
        # TODO X11 keyboard support
        import os
        filename = QFileDialog.getOpenFileName(
            self,
            "Open compiled layout file",
            directory=os.path.join(os.environ["WINDIR"], "System32", "KBDUS.DLL"),
            filter="Windows keyboard layout (*.dll);;All files (*.*)",
        )[0]
        if filename:
            open_editor(filename)

    def action_about(self, checked=False):
        with open_text(__package__, "about.ui") as layout:
            dialog = uic.loadUi(layout, QDialog(self))
            assert isinstance(dialog, QDialog)
            dialog.exec_()

    def action_license(self, checked=False):
        with open_text(__package__, "license.ui") as layout:
            dialog = uic.loadUi(layout, QDialog(self))
            assert isinstance(dialog, QDialog)
            dialog.exec_()


def main(argv):
    name = f"PyKbdEdit {_version}"

    application = QApplication(argv)
    application.setApplicationDisplayName(name)

    launcher = Launcher()
    launcher.show()

    return application.exec_()
