from dataclasses import dataclass

from PyKbd.layout import ScanCode


@dataclass(frozen=True)
class Vk:
    code: int
    name: str
    vsc: ScanCode


def _generate(f):
    ansi = [
        Vk(0x00, "kVK_ANSI_A", ScanCode(0x1E)),
        Vk(0x01, "kVK_ANSI_S", ScanCode(0x1F)),
        Vk(0x02, "kVK_ANSI_D", ScanCode(0x20)),
        Vk(0x03, "kVK_ANSI_F", ScanCode(0x21)),
        Vk(0x04, "kVK_ANSI_H", ScanCode(0x23)),
        Vk(0x05, "kVK_ANSI_G", ScanCode(0x22)),
        Vk(0x06, "kVK_ANSI_Z", ScanCode(0x2C)),
        Vk(0x07, "kVK_ANSI_X", ScanCode(0x2D)),
        Vk(0x08, "kVK_ANSI_C", ScanCode(0x2E)),
        Vk(0x09, "kVK_ANSI_V", ScanCode(0x2F)),
        # TODO 0x0A - present on Slovenian keyboard
        Vk(0x0B, "kVK_ANSI_B", ScanCode(0x30)),
        Vk(0x0C, "kVK_ANSI_Q", ScanCode(0x10)),
        Vk(0x0D, "kVK_ANSI_W", ScanCode(0x11)),
        Vk(0x0E, "kVK_ANSI_E", ScanCode(0x12)),
        Vk(0x0F, "kVK_ANSI_R", ScanCode(0x13)),
        Vk(0x10, "kVK_ANSI_Y", ScanCode(0x15)),
        Vk(0x11, "kVK_ANSI_T", ScanCode(0x14)),
        Vk(0x12, "kVK_ANSI_1", ScanCode(0x02)),
        Vk(0x13, "kVK_ANSI_2", ScanCode(0x03)),
        Vk(0x14, "kVK_ANSI_3", ScanCode(0x04)),
        Vk(0x15, "kVK_ANSI_4", ScanCode(0x05)),
        Vk(0x16, "kVK_ANSI_6", ScanCode(0x07)),
        Vk(0x17, "kVK_ANSI_5", ScanCode(0x06)),
        Vk(0x18, "kVK_ANSI_Equal", ScanCode(0x0D)),
        Vk(0x19, "kVK_ANSI_9", ScanCode(0x0A)),
        Vk(0x1A, "kVK_ANSI_7", ScanCode(0x08)),
        Vk(0x1B, "kVK_ANSI_Minus", ScanCode(0x0C)),
        Vk(0x1C, "kVK_ANSI_8", ScanCode(0x09)),
        Vk(0x1D, "kVK_ANSI_0", ScanCode(0x0B)),
        Vk(0x1E, "kVK_ANSI_RightBracket", ScanCode(0x1B)),
        Vk(0x1F, "kVK_ANSI_O", ScanCode(0x18)),
        Vk(0x20, "kVK_ANSI_U", ScanCode(0x16)),
        Vk(0x21, "kVK_ANSI_LeftBracket", ScanCode(0x1A)),
        Vk(0x22, "kVK_ANSI_I", ScanCode(0x17)),
        Vk(0x23, "kVK_ANSI_P", ScanCode(0x19)),
        Vk(0x25, "kVK_ANSI_L", ScanCode(0x26)),
        Vk(0x26, "kVK_ANSI_J", ScanCode(0x24)),
        Vk(0x27, "kVK_ANSI_Quote", ScanCode(0x28)),
        Vk(0x28, "kVK_ANSI_K", ScanCode(0x25)),
        Vk(0x29, "kVK_ANSI_Semicolon", ScanCode(0x27)),
        Vk(0x2A, "kVK_ANSI_Backslash", ScanCode(0x2B)),  # TODO maybe vsc=0x56 on ANSI?
        Vk(0x2B, "kVK_ANSI_Comma", ScanCode(0x33)),
        Vk(0x2C, "kVK_ANSI_Slash", ScanCode(0x35)),
        Vk(0x2D, "kVK_ANSI_N", ScanCode(0x31)),
        Vk(0x2E, "kVK_ANSI_M", ScanCode(0x32)),
        Vk(0x2F, "kVK_ANSI_Period", ScanCode(0x34)),
        Vk(0x32, "kVK_ANSI_Grave", ScanCode(0x56)),  # TODO difference between ANSI (vsc = 0x29) and ISO (vsc = 0x56)?
        Vk(0x41, "kVK_ANSI_KeypadDecimal", ScanCode(0x53)),
        Vk(0x43, "kVK_ANSI_KeypadMultiply", ScanCode(0x37)),
        Vk(0x45, "kVK_ANSI_KeypadPlus", ScanCode(0x4E)),
        Vk(0x47, "kVK_ANSI_KeypadClear", ScanCode(0x45)),  # numlock
        Vk(0x4B, "kVK_ANSI_KeypadDivide", ScanCode(0x35, 0xE0)),
        Vk(0x4C, "kVK_ANSI_KeypadEnter", ScanCode(0x1C, 0xE0)),
        Vk(0x4E, "kVK_ANSI_KeypadMinus", ScanCode(0x4A)),
        #Vk(0x51, "kVK_ANSI_KeypadEquals", ScanCode(0x00)),  # TODO apple only key?
        Vk(0x52, "kVK_ANSI_Keypad0", ScanCode(0x52)),
        Vk(0x53, "kVK_ANSI_Keypad1", ScanCode(0x4F)),
        Vk(0x54, "kVK_ANSI_Keypad2", ScanCode(0x50)),
        Vk(0x55, "kVK_ANSI_Keypad3", ScanCode(0x51)),
        Vk(0x56, "kVK_ANSI_Keypad4", ScanCode(0x4B)),
        Vk(0x57, "kVK_ANSI_Keypad5", ScanCode(0x4C)),
        Vk(0x58, "kVK_ANSI_Keypad6", ScanCode(0x4D)),
        Vk(0x59, "kVK_ANSI_Keypad7", ScanCode(0x47)),
        Vk(0x5B, "kVK_ANSI_Keypad8", ScanCode(0x48)),
        Vk(0x5C, "kVK_ANSI_Keypad9", ScanCode(0x49)),
    ]

    general = [
        Vk(0x24, "kVK_Return", ScanCode(0x1C)),
        Vk(0x30, "kVK_Tab", ScanCode(0x0F)),
        Vk(0x31, "kVK_Space", ScanCode(0x39)),
        Vk(0x33, "kVK_Delete", ScanCode(0x0E)),  # backspace?, TODO check
        Vk(0x35, "kVK_Escape", ScanCode(0x01)),
        Vk(0x37, "kVK_Command", ScanCode(0x5B, 0xE0)),
        Vk(0x38, "kVK_Shift", ScanCode(0x2A)),
        Vk(0x39, "kVK_CapsLock", ScanCode(0x3A)),
        Vk(0x3A, "kVK_Option", ScanCode(0x38)),
        Vk(0x3B, "kVK_Control", ScanCode(0x1D)),
        Vk(0x3C, "kVK_RightShift", ScanCode(0x36)),
        Vk(0x3D, "kVK_RightOption", ScanCode(0x38, 0xE0)),
        Vk(0x3E, "kVK_RightControl", ScanCode(0x1D, 0xE0)),
        #Vk(0x3F, "kVK_Function", ScanCode(0x00)),  # TODO ??
        #Vk(0x40, "kVK_F17", ScanCode(0x00)),  # TODO ??
        Vk(0x48, "kVK_VolumeUp", ScanCode(0x30, 0xE0)),
        Vk(0x49, "kVK_VolumeDown", ScanCode(0x2E, 0xE0)),
        Vk(0x4A, "kVK_Mute", ScanCode(0x20, 0xE0)),
        #Vk(0x4F, "kVK_F18", ScanCode(0x00)),  # TODO ??
        #Vk(0x50, "kVK_F19", ScanCode(0x00)),  # TODO ??
        #Vk(0x5A, "kVK_F20", ScanCode(0x00)),  # TODO ??
        Vk(0x60, "kVK_F5", ScanCode(0x3F)),
        Vk(0x61, "kVK_F6", ScanCode(0x40)),
        Vk(0x62, "kVK_F7", ScanCode(0X41)),
        Vk(0x63, "kVK_F3", ScanCode(0x3D)),
        Vk(0x64, "kVK_F8", ScanCode(0x42)),
        Vk(0x65, "kVK_F9", ScanCode(0x43)),
        Vk(0x67, "kVK_F11", ScanCode(0x57)),
        Vk(0x69, "kVK_F13", ScanCode(0x54)),  # snapshot
        #Vk(0x6A, "kVK_F16", ScanCode(0x00)),  # TODO ??
        #Vk(0x6B, "kVK_F14", ScanCode(0x00)),  # TODO ??
        Vk(0x6D, "kVK_F10", ScanCode(0x44)),
        # TODO 0x6E = MENU?
        Vk(0x6F, "kVK_F12", ScanCode(0x58)),
        #Vk(0x71, "kVK_F15", ScanCode(0x00)),  # TODO ??
        Vk(0x72, "kVK_Help", ScanCode(0x52, 0xE0)),
        Vk(0x73, "kVK_Home", ScanCode(0x47, 0xE0)),
        Vk(0x74, "kVK_PageUp", ScanCode(0x49, 0xE0)),
        Vk(0x75, "kVK_ForwardDelete", ScanCode(0x53, 0xE0)),  # delete?, TODO check
        Vk(0x76, "kVK_F4", ScanCode(0x3E)),
        Vk(0x77, "kVK_End", ScanCode(0x4F, 0xE0)),
        Vk(0x78, "kVK_F2", ScanCode(0x3C)),
        Vk(0x79, "kVK_PageDown", ScanCode(0x51, 0xE0)),
        Vk(0x7A, "kVK_F1", ScanCode(0x3B)),
        Vk(0x7B, "kVK_LeftArrow", ScanCode(0x4B, 0xE0)),
        Vk(0x7C, "kVK_RightArrow", ScanCode(0x4D, 0xE0)),
        Vk(0x7D, "kVK_DownArrow", ScanCode(0x50, 0xE0)),
        Vk(0x7E, "kVK_UpArrow", ScanCode(0x48, 0xE0)),
    ]

    iso = [
        Vk(0x0A, "kVK_ISO_Section", ScanCode(0x29)),
    ]

    #jis = [
    #    Vk(0x5D, "kVK_JIS_Yen", ScanCode(0x7D)),  # TODO, T7D -> OEM_5?
    #    Vk(0x5E, "kVK_JIS_Underscore", ScanCode(0x73)),  # TODO ABNT_C?
    #    Vk(0x5F, "kVK_JIS_KeypadComma", 0x0),  # TODO apple only key?
    #    Vk(0x66, "kVK_JIS_Eisu", ScanCode(0x7B)),  # TODO "alphanumeric", left of space, apple only
    #    Vk(0x68, "kVK_JIS_Kana", ScanCode(0x79)),  # TODO right of space, apple only
    #]

    all = [*ansi, *general, *iso]
    all.sort(key=lambda vk: vk.code)

    vsc_to_vk = {key.vsc: key.name for key in all}

    for key in all:
        print(f"{key.name} = {key!r}", file=f)
    print(file=f)

    print("all = [", file=f)
    for key in all:
        print(f"    {key.name},", file=f)
    print("]", file=f)
    print(file=f)

    print("vsc_to_vk = {", file=f)
    for vsc, name in sorted(vsc_to_vk.items()):
        print(f"    {vsc}: {name},", file=f)
    print("}", file=f)


if __name__ == '__main__':
    def _main():
        import sys
        dir, sep, file = __file__.rpartition("_gen_")
        if sep != "_gen_":
            raise RuntimeError("This is the generated file. "
                               "Please run the _gen_ version to regenerate it.")

        if len(sys.argv) != 1:
            # TODO use mac SDK?
            #  raise RuntimeError("Please provide exactly one argument, path to WinUser.h.")
            raise RuntimeError("Please provide no arguments.")

        # with open(sys.argv[1], "r", encoding="ascii", errors="strict") as f:
        #     winuser = f.readlines()

        with open(dir + file, "w", encoding="ascii", errors="strict") as f:
            print("# ----- DO NOT EDIT THIS GENERATED FILE -----", file=f)
            print(file=f)
            with open(__file__, "r", encoding="ascii", errors="strict") as s:
                f.write(s.read())
            print(file=f)
            _generate(f)

    _main()

# ----- start generated content -----
