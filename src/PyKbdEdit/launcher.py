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

import os
import random
import string
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow

from . import _version
from ._util import connect, load_layout
from .editor import open_editor

__version__ = _version


class Launcher(QMainWindow):
    def __init__(self):
        super(Launcher, self).__init__()

        load_layout(self, __name__)
        connect(self)

    @staticmethod
    def action_new():
        from PyKbd.layout import Layout
        open_editor(Layout(
            name="Unnamed Layout",
            author=os.environ.get("USER", ""),
            copyright=f"Copyright (c) {datetime.now().year} {os.environ.get('USER', '')}",
            version=(1, 0),
            dll_name=f"kbd_{''.join(random.choice(string.ascii_lowercase) for _ in range(4))}.dll",
        )).action_metadata()

    def action_open(self):
        filename = QFileDialog.getOpenFileName(
            self, "Open layout file", filter="Layout Files (*.json);;All Files (*.*)"
        )[0]
        if filename:
            open_editor(filename)

    def action_decompile(self):
        # TODO X11 keyboard support
        filename = QFileDialog.getOpenFileName(
            self,
            "Open compiled layout file",
            directory=os.path.join(os.environ["WINDIR"], "System32", "KBDUS.DLL"),
            filter="Windows Keyboard Layouts (*.dll);;All Files (*.*)",
        )[0]
        if filename:
            from PyKbd.compile_windll import WinDll

            windll = WinDll()
            with open(filename, "rb") as f:
                windll.decompile(f.read())
            open_editor(windll.layout).action_metadata()

    def action_about(self):
        dialog = load_layout(QDialog(self), f"{__package__}.about")
        assert isinstance(dialog, QDialog)
        dialog.open()

    def action_license(self):
        dialog = load_layout(QDialog(self), f"{__package__}.license")
        assert isinstance(dialog, QDialog)
        dialog.open()


def main(argv):
    name = f"PyKbdEdit {_version}"

    application = QApplication(argv)
    application.setApplicationDisplayName(name)

    launcher = Launcher()
    launcher.show()

    return application.exec_()
