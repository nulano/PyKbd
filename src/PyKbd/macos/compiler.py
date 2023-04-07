import io
from typing import Optional
from warnings import warn

from lxml import etree

from PyKbd import __version__
from PyKbd.data import mac_vk, win_vk
from PyKbd.layout import Layout, KeyCode, ShiftState, Character, KeyAttributes

DOCTYPE = '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">'


def compile_keylayout(layout: Layout) -> str:
    f = io.BytesIO()
    with etree.xmlfile(f, encoding="utf-8") as xf:
        xf.write_declaration(doctype=DOCTYPE)
        # TODO add attribute maxout, optional?
        with xf.element(
                "keyboard",
                group="126",
                id=f"-{''.join(str(ord(c)) for c in layout.dll_name[3:-4])}",
                name=f"{layout.name} (version {'.'.join(map(str, layout.version))})",
        ):
            xf.write(etree.Comment("Generated with PyKbd %s" % (__version__,)))

            # all physical keyboards map to the same VKs with minimal overlap (only \| key on ANSI/ISO)
            # define only a single layout to use for all keyboards
            with xf.element("layouts"):
                xf.write(etree.Element("layout", first="0", last="0", modifiers="modifiers", mapSet="mapSet"))

            # convert layout to macOS format (i.e. invert tables)
            charmap = convert_layout(layout)

            modifiers = list(convert_attributes_to_shift_map(KeyAttributes()).keys())
            with xf.element("modifierMap", id="modifiers", defaultIndex="0"):
                for i, m in enumerate(modifiers):
                    with xf.element("keyMapSelect", mapIndex=str(i)):
                        xf.write(etree.Element("modifier", keys=m))

            def when(state, result):
                state = "none" if state is None else f"d{state.encode('utf-8').hex()}"
                if result.dead:
                    next_ = f"d{result.char.encode('utf-8').hex()}"
                    xf.write(etree.Element("when", state=state, next=next_))
                else:
                    output = "".join(c if 32 <= ord(c) <= 127 and c not in '\n\r\t"<>&' else f"&#{ord(c)};"
                                     for c in result.char)  # TODO it seems null bytes sometimes appear
                    # output = result.char
                    xf.write(etree.Element("when", state=state, output=output))

            with xf.element("keyMapSet", id="mapSet"):
                for i, m in enumerate(modifiers):
                    with xf.element("keyMap", index=str(i)):
                        for mvk, column in charmap.items():
                            action = column.get(m)
                            if action is None:
                                continue
                            # TODO no need for <action> element if len(action) == 1
                            with xf.element("key", code=str(mvk.code)):
                                with xf.element("action"):
                                    for state, result in action.items():
                                        when(state, result)

            # no need for <actions> element, all are anonymous

            with xf.element("terminators"):
                for dead in layout.deadkeys:
                    when(dead, Character(dead))

    f.seek(0)
    tree = etree.parse(f)
    text = etree.tostring(tree, encoding="utf-8", xml_declaration=True, pretty_print=True)
    return text.decode("utf-8").replace("&amp;", "&")


def convert_layout(layout: Layout) -> dict[mac_vk.Vk, dict[str, dict[Optional[str], Character]]]:
    charmap = {}
    for mvk in mac_vk.all:
        keycode = layout.keymap.get(mvk.vsc)
        if keycode is None:
            warn("no mapping for " + mvk.name)
            continue
        vk = KeyCode.translate_vk(keycode.win_vk)
        vk &= ~0x100  # drop KBDEXT flag
        wvk = win_vk.code_to_vk.get(vk)
        action = layout.charmap.get(vk, {})
        if len(action) == 0:
            # add default mappings for some control keys not needed on Windows
            control = {
                win_vk.VK_HOME: "\x01",
                win_vk.VK_END: "\x04",
                win_vk.VK_INSERT: "\x05",
                win_vk.VK_PRIOR: "\x0b",
                win_vk.VK_NEXT: "\x0c",
                win_vk.VK_NUMLOCK: "\x1b",  # kVK_ANSI_KeypadClear
                win_vk.VK_NUMLOCK_MULTIVK: "\x1b",  # kVK_ANSI_KeypadClear
                win_vk.VK_LEFT: "\x1c",
                win_vk.VK_RIGHT: "\x1d",
                win_vk.VK_UP: "\x1e",
                win_vk.VK_DOWN: "\x1f",
                win_vk.VK_DELETE: "\x7f",
                # TODO these may be needed on Windows, macOS might need different mappings, not sure
                # win_vk.VK_RETURN: "\x0d",
                # win_vk.VK_TAB: "\x09",
                # win_vk.VK_BACK: "\x08",
                # win_vk.VK_ESCAPE: "\x1b",
            }.get(wvk)
            if win_vk.VK_F1 <= wvk <= win_vk.VK_F24:
                control = "\x10"
            # TODO unknown mac_vk mappings:
            #  52 -> \x03
            #  66 -> \x1d,*
            #  70 -> \x1c,+
            #  72 -> \x1f,= (volume up)
            #  76 -> \x03? (numpad enter)
            #  77 -> \x1e,/
            #  81 -> = (numpad equals)
            #  105 -> \x10 (f13)
            if control is not None:
                charmap[mvk] = {mac_state: convert_character(layout, Character(control))
                                for mac_state in convert_attributes_to_shift_map(keycode.attributes)}
                continue
            # print(f"{mvk!r} -> {vk.to_bytes(2, 'big').hex()}, {wvk!r}")
        if vk in (0, 0xFF):
            continue
        elif vk > 0xFF:
            warn("unknown special vk, skipping: 0x%X" % vk)
            continue
        charmap[mvk] = {mac_state: convert_character(layout, action[win_state])
                        for mac_state, win_state in convert_attributes_to_shift_map(keycode.attributes).items()
                        if win_state in action}
    return charmap


def convert_character(layout: Layout, character: Character) -> dict[Optional[str], Character]:
    out = {None: character}
    for dead, deadmap in layout.deadkeys.items():
        try:
            out[dead] = deadmap.charmap[character.char]
        except KeyError:
            pass
    return out


def convert_attributes_to_shift_map(attributes: KeyAttributes):
    """
    Return shift state conversion map for KeyAttributes.
    Not all Windows shift states are accessible via a macOS shift state.
    macOS shift states are fixed.
    """
    # supported modifiers are:
    # - shift, rightShift, anyShift
    # - option, rightOption, anyOption
    # - control, rightControl, anyControl
    # - command, caps
    # there is no Kana modifier

    # the default conversion is somewhat limited:
    #   option = ctrl+alt i.e. alt gr
    #   command has no effect
    #   control

    # map macOS shift state + keycode.attribute to Windows shift state
    translation = {
        "command?": ShiftState(),
        "command? anyShift": ShiftState(shift=True),
        "command? anyOption": ShiftState(control=True, alt=True),
        "command? anyShift anyOption": ShiftState(shift=True, control=True, alt=True),
        "command? control anyShift? anyOption? caps?": ShiftState(control=True),
    }

    if not attributes.capslock:
        translation.update({
            "command? caps": ShiftState(),
            "command? caps anyShift": ShiftState(shift=True),
        })
    elif not attributes.capslock_secondary:  # TODO how does this combine with capslock?
        translation.update({
            "command? caps": ShiftState(shift=True),
            "command? caps anyShift": ShiftState(),
        })
    else:
        translation.update({
            "command? caps": ShiftState(capslock=True),
            "command? caps anyShift": ShiftState(shift=True, capslock=True),
        })

    if not attributes.capslock_altgr:
        translation.update({
            "command? anyOption caps": ShiftState(control=True, alt=True),
            "command? anyOption caps anyShift": ShiftState(shift=True, control=True, alt=True),
        })
    elif not attributes.capslock_secondary:
        translation.update({
            "command? anyOption caps": ShiftState(shift=True, control=True, alt=True),
            "command? anyOption caps anyShift": ShiftState(control=True, alt=True),
        })
    else:
        translation.update({
            "command? anyOption caps": ShiftState(control=True, alt=True, capslock=True),
            "command? anyOption caps anyShift": ShiftState(shift=True, control=True, alt=True, capslock=True),
        })

    return translation


if __name__ == '__main__':
    with open("../../../kbddvp_3.5.json", "r", encoding="utf-8") as f:
        data = f.read()

    layout = Layout.from_json(data)

    print(compile_keylayout(layout))
