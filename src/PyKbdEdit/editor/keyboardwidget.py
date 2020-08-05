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

from collections import defaultdict
from typing import Dict, List, Tuple, Callable, Any

from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel

from PyKbd.layout import ScanCode
from PyKbd.visualizer import Keyboard


class KeyboardWidget(QWidget):
    clicked: Callable[[ScanCode], Any]
    """Button click callback."""
    style: Callable[[ScanCode], Tuple[str, str, str, bool, bool, str]]
    """Button style. Returns (text, color, borderColor, selected, disabled, extra)"""
    keySizeHint = 100
    keySizeHintMin = 20

    _keyboard: Keyboard
    _scale = 1.0
    _padding = (0.0, 0.0)
    _bounds = (0.0, 0.0, 0.0, 0.0)
    _keys: Dict[ScanCode, List[Tuple[Tuple[float, float, float, float], bool, QPushButton]]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._keys = defaultdict(list)

        # placeholder callbacks
        self.clicked = lambda scancode: print(scancode)
        self.style = lambda scancode: (scancode.to_string(), "#faa", "#6aa", False, False, "")

        # initialize with blank layout
        self.keyboard = None

    @property
    def keyboard(self):
        return self._keyboard

    @keyboard.setter
    def keyboard(self, kbd):
        if kbd is None:
            kbd = Keyboard("None", [])
        self._keyboard = kbd
        self._bounds = kbd.bounds()
        for keys in self._keys.values():
            for bounds, special, key in keys:
                key.setParent(None)
        self._keys.clear()
        for bounds, scancode, special in kbd:
            btn = QPushButton("?", self)
            btn.show()
            btn.setFlat(True)
            btn.setMinimumSize(0, 0)
            btn.clicked.connect(lambda c, s=scancode: self.clicked(s))
            self._keys[scancode].append((bounds, special, btn))
        self.updateGeometry()
        # force a reload
        self.reload(geometry=True)

    def update_keys(self, scancode: ScanCode, geometry=False):
        s = self._scale
        px, py = self._padding
        ox, oy, _, _ = self._bounds
        fnt = None
        for bounds, special, key in self._keys[scancode]:
            text, color, borderColor, selected, disabled, extra = self.style(scancode)
            text_changed = text != key.text()
            key.setText(text)
            key.setEnabled(not disabled)
            if selected:
                style = f"""
QPushButton {{
  background-color: {color};
  border: 5px solid {borderColor};
}}
"""
            else:
                style = f"""
QPushButton {{
  background-color: {color};
  border: 1px solid {borderColor};
}}
QPushButton:hover, QPushButton:focus {{
  border: 3px dotted {borderColor};
}}
QPushButton:disabled {{
  color: #222;
}}
"""
            key.setStyleSheet(style + extra)
            if geometry or text_changed:
                x1, y1, x2, y2 = bounds
                x, y, w, h = x1 - ox, y1 - oy, x2 - x1, y2 - y1
                key.setGeometry(px + x * s, py + y * s, w * s, h * s)
                if fnt is None:
                    fnt = self.font()
                    fnt_pointSizeF = fnt.pointSizeF()
                    fm = self.fontMetrics()
                fnt.setPointSizeF(
                    fnt_pointSizeF * min(
                        (h * s - 10) / fm.lineSpacing(),
                        (w * s - 10) / (fm.horizontalAdvance(text) or 1),
                    ) * 0.95
                )
                key.setFont(fnt)

    def reload(self, geometry=False):
        if geometry:
            size = self.size()
            w, h = size.width(), size.height()
            x1, y1, x2, y2 = self._bounds
            if x1 == x2 or y1 == y2:
                self._scale = min(w, h)
            else:
                self._scale = min(w / (x2 - x1), h / (y2 - y1))
            self._padding = (w - self._scale * (x2 - x1)) / 2, (h - self._scale * (y2 - y1)) / 2
        for scancode in self._keys:
            self.update_keys(scancode, geometry=geometry)

    def resizeEvent(self, ev):
        super(KeyboardWidget, self).resizeEvent(ev)
        self.reload(geometry=True)

    def sizeHint(self):
        keySize = self.keySizeHint
        x1, y1, x2, y2 = self._bounds
        return QSize(int((x2 - x1) * keySize), int((y2 - y1) * keySize))

    def minimumSizeHint(self):
        keySize = self.keySizeHintMin
        x1, y1, x2, y2 = self._bounds
        return QSize(int((x2 - x1) * keySize), int((y2 - y1) * keySize))
