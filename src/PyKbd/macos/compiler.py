import io
from typing import Optional
from warnings import warn

from lxml import etree

from PyKbd.data import mac_vk
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

            # all physical keyboards map to the same VKs with minimal overlap (only \| key on ANSI/ISO)
            # define only a single layout to use for all keyboards
            with xf.element("layouts"):
                xf.write(etree.Element("layout", first="0", last="0", modifiers="modifiers", mapSet="mapSet"))

            # convert layout to macOS format (i.e. invert tables)
            charmap = convert_layout(layout)
            # TODO may need to add extra control mappings that are not needed on Windows

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
                                     for c in result.char if c != "\0")
                    # output = result.char
                    xf.write(etree.Element("when", state=state, output=output))

            with xf.element("keyMapSet", id="mapSet"):
                for i, m in enumerate(modifiers):
                    with xf.element("keyMap", index=str(i)):
                        for mvk, column in charmap.items():
                            action = column.get(m)
                            if action is None:
                                continue  # TODO may need to add some default control chars
                            # TODO no need for <action> element if len(action) == 1
                            with xf.element("key", code=str(mvk.code)):
                                with xf.element("action"):
                                    for state, result in action.items():
                                        when(state, result)

            # no need for <actions> element, all are anonymous

            with xf.element("terminators"):
                for dead in layout.deadkeys:
                    when(dead, Character(dead))

    return etree.tostring(etree.fromstring(f.getvalue()), pretty_print=True).decode("utf-8").replace("&amp;", "&")


def convert_layout(layout: Layout) -> dict[mac_vk.Vk, dict[str, dict[Optional[str], Character]]]:
    charmap = {}
    for mvk in mac_vk.all:
        keycode = layout.keymap.get(mvk.vsc)
        if keycode is None:
            warn("no mapping for " + mvk.name)
            continue
        vk = KeyCode.translate_vk(keycode.win_vk)
        if vk in (0, 0xFF) or len(layout.charmap.get(vk, {})) == 0:
            continue
        elif vk > 0xFF:
            warn("unknown special vk, skipping: 0x%X" % vk)
            continue
        charmap[mvk] = {mac_state: convert_character(layout, layout.charmap[vk][win_state])
                        for mac_state, win_state in convert_attributes_to_shift_map(keycode.attributes).items()
                        if win_state in layout.charmap[vk]}
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
