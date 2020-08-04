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

import inspect
import string
from importlib.resources import open_text

from PyQt5 import uic
from PyQt5.QtWidgets import QAction, QWidget, QPushButton


def load_layout(wnd: QWidget, name: str):
    """
    :param wnd: The QWidget to populate.
    :param name: __name__ or layout name in similar format.
    """
    package, _, name = name.rpartition('.')
    with open_text(package, name + ".ui") as layout:
        uic.loadUi(layout, wnd)


def connect(wnd: QWidget):
    """
    Connects ``wnd.action_foo_bar(wnd)`` to ``wnd.actionFooBar`` QActions.
    The method may optionally take a ``checked`` parameter (name required).

    Connects ``wnd.btn_foo_bar(wnd)`` to ``wnd.btnFooBar`` QPushButtons.
    The method may optionally take a ``checked`` parameter (name required).
    """
    for name, func in wnd.__class__.__dict__.items():
        name2 = name[0].lower() + string.capwords(name, sep="_").replace("_", "")[1:]
        target = getattr(wnd, name2, None)
        if name[:7] == "action_":
            assert isinstance(target, QAction)
            assert callable(func) or isinstance(func, (staticmethod, classmethod))
            func = func.__get__(wnd, wnd.__class__)
            if "checked" in inspect.signature(func).parameters:
                target.triggered.connect(lambda checked, f=func: f(checked=checked))
            else:
                target.triggered.connect(lambda checked, f=func: f())
        elif name[:4] == "btn_":
            assert isinstance(target, QPushButton)
            assert callable(func) or isinstance(func, (staticmethod, classmethod))
            func = func.__get__(wnd, wnd.__class__)
            if "checked" in inspect.signature(func).parameters:
                target.clicked.connect(lambda checked, f=func: f(checked=checked))
            else:
                target.clicked.connect(lambda checked, f=func: f())
