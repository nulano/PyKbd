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

from typing import Union

from PyQt5.QtWidgets import QFileDialog, QMainWindow

from PyKbd.layout import Layout

from .._util import connect, load_layout
from . import _version
from .metadata import MetadataWindow
from .keyboardwidget import KeyboardWidget

__version__ = _version


class EditorWindow(QMainWindow):
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

    def closeEvent(self, ev):
        print("closing...")
        ev.accept()

    def load_metadata(self):
        self.setWindowTitle(self.kbd_layout.name)

    def action_save(self):
        if not self.filename:
            self.action_save_as("Save Layout...")
        else:
            print("saved as", self.filename)

    def action_save_as(self, caption="Save Layout As..."):
        filename = QFileDialog.getSaveFileName(
            self, caption, self.filename, "Layout Files (*.json);;All Files (*.*)"
        )[0]
        if filename:
            self.filename = filename
            self.action_save()

    def action_metadata(self):
        dlg = MetadataWindow(self, self.kbd_layout)
        dlg.accepted.connect(self.load_metadata)
        dlg.open()
