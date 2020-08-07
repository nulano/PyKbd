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
from collections import defaultdict
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
        return uic.loadUi(layout, wnd)


def connected(*args, **kwargs):
    def wrap(func):
        func.connected = (args, kwargs)
        return func

    wrap.connected_wrap = inspect.stack()[1]
    return wrap


def connect(wnd: QWidget):
    """
    Connects ``@connected``-decorated ``myObject_mySignal`` methods of ``wnd``
    to ``wnd.myObject``'s signal ``mySignal``.

    ``mySignal`` name is optional for ``QAction.triggered`` and ``QPushButton.clicked``.
    """
    for name, func in wnd.__class__.__dict__.items():
        if hasattr(func, "connected"):
            func = func.__get__(wnd, wnd.__class__)
            params = inspect.signature(func).parameters

            target, _, action = name.partition("_")
            target = getattr(wnd, target)
            if action == "":
                if isinstance(target, QAction):
                    action = "triggered"
                elif isinstance(target, QPushButton):
                    action = "clicked"
            action = getattr(target, action)
            action.connect(func)
        elif hasattr(func, "connected_wrap"):
            stack = getattr(func, "connected_wrap")
            raise TypeError(f"function {name} is connected without parameters\n"
                            f"  in File \"{stack.filename}\", line {stack.lineno}, in {stack.function}")
