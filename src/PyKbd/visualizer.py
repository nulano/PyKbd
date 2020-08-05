# This file is part of PyKbd
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

from dataclasses import dataclass
from math import sqrt
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from PyKbd.layout import KeyCode, Layout, ScanCode, ShiftState


@dataclass(frozen=True)
class Row:
    left_width: float = 0
    left: Optional[int] = None
    keys: List[int] = ()
    right: Optional[int] = None
    right_width: float = 0


@dataclass(frozen=True)
class Group:
    rows: List[Row]
    prefix: int = 0
    width: float = 1
    height: float = 1
    special: bool = True


@dataclass(frozen=True)
class Keyboard:
    name: str
    groups: List[Tuple[float, float, Group]]

    def bounds(self):
        x1, y1, x2, y2 = 100, 100, -100, -100
        for ox, oy, group in self.groups:
            y1 = min(y1, oy)
            y2 = max(y2, oy + group.height)
            for row in group.rows:
                x1 = min(x1, ox)
                x2 = max(x2, ox + row.left_width + len(row.keys) * group.width + row.right_width)
        if x1 >= x2 or y1 >= y2:
            return 0, 0, 0, 0
        return x1, y1, x2, y2

    def __iter__(self):
        for ox, oy, group in self.groups:
            for row in group.rows:
                x = ox
                if row.left is not None:
                    yield (
                        (x, oy, x + row.left_width, oy + group.height),
                        ScanCode(row.left, group.prefix),
                        True,
                    )
                x += row.left_width
                for key in row.keys:
                    yield (
                        (x, oy, x + group.width, oy + group.height),
                        ScanCode(key, group.prefix),
                        group.special,
                    )
                    x += group.width
                if row.right is not None:
                    yield (
                        (x, oy, x + row.right_width, oy + group.height),
                        ScanCode(row.right, group.prefix),
                        True,
                    )
                oy += group.height


_function = [
    # Function Keys
    (0, 0.5, Group([Row(1.50, 0x01)])),
    (2, 0.5, Group([Row(keys=[0x3B, 0x3C, 0x3D, 0x3E])])),
    (6.5, 0.5, Group([Row(keys=[0x3F, 0x40, 0x41, 0x42])])),
    (11, 0.5, Group([Row(keys=[0x43, 0x44, 0x57, 0x58])])),
    (15.5, 0.5, Group([Row(keys=[0x37])], 0xE0)),
    (16.5, 0.5, Group([Row(keys=[0x46])])),
    (17.5, 0.5, Group([Row(keys=[0x1D])], 0xE1)),
]

_main_ansi = [
    # Main
    (0, 2, Group([
        Row(0.00, None, [0x29, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D], 0x0E, 2.00),
        Row(1.50, 0x0F,       [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B]            ),
        Row(1.75, 0x3A,       [0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28],       0x1C, 2.25),
        Row(2.25, 0x2A,       [0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35],             0x36, 2.75),
    ], special=False)),
    # VK_OEM_5 ('\|' on US keyboard) is extra wide, but not special
    (13.5, 3, Group([Row(0.00, None, [0x2B])], width=1.50, special=False)),
]

_main_iso = [
    # Main
    (0, 2, Group([
        Row(0.00, None, [0x29, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D], 0x0E, 2.00),
        Row(1.50, 0x0F,       [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B], 0x1C, 1.50),
        Row(1.75, 0x3A,       [0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x2B], 0x1C, 1.25),
        Row(1.25, 0x2A, [0x56, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35],             0x36, 2.75),
    ], special=False)),
]

_bottom = [
    # bottom row for 104/105 and 87/88 keyboards
    (00.00, 6, Group([Row(1.50, 0x1D)])),
    (01.50, 6, Group([Row(1.25, 0x5B)], 0xE0)),
    (02.75, 6, Group([Row(1.25, 0x38)])),
    (04.00, 6, Group([Row(6.00, 0x39)])),
    (10.00, 6, Group([Row(1.25, 0x38)], 0xE0)),
    (11.25, 6, Group([Row(1.25, 0x5C)], 0xE0)),
    (12.50, 6, Group([Row(1.25, 0x5D)], 0xE0)),
    (13.75, 6, Group([Row(1.25, 0x1D)], 0xE0)),
]

_bottom_101 = [
    # bottom row for 101/102 (IBM) keyboards
    (00.00, 6, Group([Row(1.50, 0x1D)])),
    # (blank space of width 1 key)
    (02.75, 6, Group([Row(1.25, 0x38)])),
    (04.00, 6, Group([Row(7.00, 0x39)])),
    (11.00, 6, Group([Row(1.50, 0x38)], 0xE0)),
    # (blank space of width 1 key)
    (13.50, 6, Group([Row(1.50, 0x1D)], 0xE0)),
]

_navigation = [
    # Navigation
    (15.5, 2, Group([
        Row(keys=[0x52, 0x47, 0x49]),
        Row(keys=[0x53, 0x4F, 0x51]),
    ], 0xE0)),
    (16.5, 5, Group([Row(keys=[0x48])], 0xE0)),
    (15.5, 6, Group([Row(keys=[0x4B, 0x50, 0x4D])], 0xE0)),
]

_numpad = [
    # Numpad
    (19, 2, Group([Row(keys=[0x45])])),
    (20, 2, Group([Row(keys=[0x35])], 0xE0, special=False)),
    (21, 2, Group([Row(keys=[0x37, 0x4A])], special=False)),
    (19, 3, Group([
        Row(keys=[0x47, 0x48, 0x49]),
        Row(keys=[0x4B, 0x4C, 0x4D]),
        Row(keys=[0x4F, 0x50, 0x51]),
        Row(2, 0x52, [0x53]),
    ], special=False)),
    (22, 3, Group([Row(keys=[0x4E])], height=2, special=False)),
    (22, 5, Group([Row(keys=[0x1C])], 0xE0, height=2)),
]

# ANSI keyboards

ANSI_104 = Keyboard("ANSI 104-key", [
    *_function,
    *_main_ansi,
    *_bottom,
    *_navigation,
    *_numpad,
])
ANSI_101 = Keyboard("ANSI 101-key", [
    *_function,
    *_main_ansi,
    *_bottom_101,
    *_navigation,
])
ANSI_87 = Keyboard("ANSI 87-key", [
    *_function,
    *_main_ansi,
    *_bottom,
    *_navigation,
])
ANSI_61 = Keyboard("ANSI 61-key", [
    *_main_ansi,
    *_bottom,
])

# ISO keyboards

ISO_105 = Keyboard("ISO 105-key", [
    *_function,
    *_main_iso,
    *_bottom,
    *_navigation,
    *_numpad,
])
ISO_102 = Keyboard("ISO 102-key", [
    *_function,
    *_main_iso,
    *_bottom_101,
    *_navigation,
    *_numpad,
])
ISO_88 = Keyboard("ISO 88-key", [
    *_function,
    *_main_iso,
    *_bottom,
    *_navigation,
])
ISO_62 = Keyboard("ISO 62-key", [
    *_main_iso,
    *_bottom,
])

NUMPAD = Keyboard("Numpad", _numpad)


ANSI = ANSI_104
ISO = ISO_105

all = [
    ANSI_104, ANSI_101, ANSI_87, ANSI_61,
    ISO_105, ISO_102, ISO_88, ISO_62,
    NUMPAD,
]


def draw_text(draw, x, y, font, text, color=(0, 0, 0)):
    xs, ys = font.getsize(text)
    draw.text((x - xs / 2, y - ys / 2), text, fill=color, font=font)


def draw_key(x, y, w, h, draw: ImageDraw, layout: Layout, key: ScanCode, font: ImageFont, hide_name: bool = False):
    draw.rectangle((x, y, x + w, y + h), outline=(0, 0, 0))
    keycode = layout.keymap.get(key)
    if keycode is None:
        return
    vk = KeyCode.translate_vk(keycode.win_vk)
    if vk not in layout.charmap:
        draw_text(draw, x + w / 2, y + h / 2, font, keycode.name or "0x%X" % keycode.win_vk, color=(0, 0, 192))
    else:
        characters = layout.charmap[vk]
        for shiftstate, px, py in [
            (ShiftState(shift=True,  control=False, alt=False), 0.2, 0.25),
            (ShiftState(shift=False, control=False, alt=False), 0.2, 0.75),
            (ShiftState(shift=True,  control=True,  alt=False), 0.5, 0.25),
            (ShiftState(shift=False, control=True,  alt=False), 0.5, 0.75),
            (ShiftState(shift=True,  control=True,  alt=True ), 0.8, 0.25),
            (ShiftState(shift=False, control=True,  alt=True ), 0.8, 0.75),
        ]:
            if shiftstate in characters:
                character = characters[shiftstate]
                text = character.char
                color = (255, 0, 0) if character.dead else (0, 0, 0)
                if ord(character.char) < 0x20:
                    text = '^' + chr(ord(character.char) + 0x40)
                    color = (255, 128, 0) if character.dead else (0, 128, 0)
                draw_text(draw, x + px * w, y + py * h, font, text, color)


def draw_keyboard(layout: Layout, keyboard: Keyboard):
    key_size = 100
    minx, miny, maxx, maxy = keyboard.bounds()
    if (minx, miny, maxx, maxy) == (0, 0, 0, 0):
        return Image.new("RGB", (0, 0))
    miny -= 0.5  # title
    wd, ht = int((maxx - minx) * key_size + 1), int((maxy - miny) * key_size + 1)
    im = Image.new("RGB", (wd, ht), (255, 255, 255))
    draw = ImageDraw.Draw(im, "RGB")
    font = ImageFont.truetype('segoeui', 24)
    draw_text(draw, (maxx - minx) * key_size / 2, 0.25 * key_size, font, layout.name + " by " + layout.author)
    for bounds, scancode, special in keyboard:
        x1, y1, x2, y2 = bounds
        draw_key(
            (x1 - minx) * key_size,
            (y1 - miny + 0.5) * key_size,
            (x2 - x1) * key_size,
            (y2 - y1) * key_size,
            draw,
            layout,
            scancode,
            font,
            not special,
        )
    return im


def draw_dead_keys(layout: Layout):
    import networkx as nx
    import matplotlib.pyplot as plt

    edge_labels = {}

    G = nx.DiGraph()
    G.add_nodes_from(layout.deadkeys.keys())
    for accent, characters in layout.deadkeys.items():
        for character, result in characters.charmap.items():
            if result.char == '\0':
                continue
            G.add_node(result.char)
            edge_labels[(accent, result.char)] = character
    G.add_edges_from(edge_labels.keys(), weight=1)
    print("num edges: %d" % len(edge_labels))

    plt.figure(figsize=(2 * sqrt(len(G.nodes)), 2 * sqrt(len(G.nodes))))
    try:
        # good params: dot, sfdp
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot', args='-Ksfdp')
    except ImportError:
        try:
            pos = nx.kamada_kawai_layout(G)
        except ImportError:
            pos = nx.spring_layout(G)
    nx.draw(G, pos, node_size=200, node_color='0.7')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='Segoe UI')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10, font_family='Segoe UI')
    canvas = plt.get_current_fig_manager().canvas
    canvas.draw()
    im = Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    # plt.show()
    return im
