# ----- DO NOT EDIT THIS GENERATED FILE -----

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

kVK_ANSI_A = Vk(code=0, name='kVK_ANSI_A', vsc=ScanCode(prefix=0, code=30))
kVK_ANSI_S = Vk(code=1, name='kVK_ANSI_S', vsc=ScanCode(prefix=0, code=31))
kVK_ANSI_D = Vk(code=2, name='kVK_ANSI_D', vsc=ScanCode(prefix=0, code=32))
kVK_ANSI_F = Vk(code=3, name='kVK_ANSI_F', vsc=ScanCode(prefix=0, code=33))
kVK_ANSI_H = Vk(code=4, name='kVK_ANSI_H', vsc=ScanCode(prefix=0, code=35))
kVK_ANSI_G = Vk(code=5, name='kVK_ANSI_G', vsc=ScanCode(prefix=0, code=34))
kVK_ANSI_Z = Vk(code=6, name='kVK_ANSI_Z', vsc=ScanCode(prefix=0, code=44))
kVK_ANSI_X = Vk(code=7, name='kVK_ANSI_X', vsc=ScanCode(prefix=0, code=45))
kVK_ANSI_C = Vk(code=8, name='kVK_ANSI_C', vsc=ScanCode(prefix=0, code=46))
kVK_ANSI_V = Vk(code=9, name='kVK_ANSI_V', vsc=ScanCode(prefix=0, code=47))
kVK_ISO_Section = Vk(code=10, name='kVK_ISO_Section', vsc=ScanCode(prefix=0, code=41))
kVK_ANSI_B = Vk(code=11, name='kVK_ANSI_B', vsc=ScanCode(prefix=0, code=48))
kVK_ANSI_Q = Vk(code=12, name='kVK_ANSI_Q', vsc=ScanCode(prefix=0, code=16))
kVK_ANSI_W = Vk(code=13, name='kVK_ANSI_W', vsc=ScanCode(prefix=0, code=17))
kVK_ANSI_E = Vk(code=14, name='kVK_ANSI_E', vsc=ScanCode(prefix=0, code=18))
kVK_ANSI_R = Vk(code=15, name='kVK_ANSI_R', vsc=ScanCode(prefix=0, code=19))
kVK_ANSI_Y = Vk(code=16, name='kVK_ANSI_Y', vsc=ScanCode(prefix=0, code=21))
kVK_ANSI_T = Vk(code=17, name='kVK_ANSI_T', vsc=ScanCode(prefix=0, code=20))
kVK_ANSI_1 = Vk(code=18, name='kVK_ANSI_1', vsc=ScanCode(prefix=0, code=2))
kVK_ANSI_2 = Vk(code=19, name='kVK_ANSI_2', vsc=ScanCode(prefix=0, code=3))
kVK_ANSI_3 = Vk(code=20, name='kVK_ANSI_3', vsc=ScanCode(prefix=0, code=4))
kVK_ANSI_4 = Vk(code=21, name='kVK_ANSI_4', vsc=ScanCode(prefix=0, code=5))
kVK_ANSI_6 = Vk(code=22, name='kVK_ANSI_6', vsc=ScanCode(prefix=0, code=7))
kVK_ANSI_5 = Vk(code=23, name='kVK_ANSI_5', vsc=ScanCode(prefix=0, code=6))
kVK_ANSI_Equal = Vk(code=24, name='kVK_ANSI_Equal', vsc=ScanCode(prefix=0, code=13))
kVK_ANSI_9 = Vk(code=25, name='kVK_ANSI_9', vsc=ScanCode(prefix=0, code=10))
kVK_ANSI_7 = Vk(code=26, name='kVK_ANSI_7', vsc=ScanCode(prefix=0, code=8))
kVK_ANSI_Minus = Vk(code=27, name='kVK_ANSI_Minus', vsc=ScanCode(prefix=0, code=12))
kVK_ANSI_8 = Vk(code=28, name='kVK_ANSI_8', vsc=ScanCode(prefix=0, code=9))
kVK_ANSI_0 = Vk(code=29, name='kVK_ANSI_0', vsc=ScanCode(prefix=0, code=11))
kVK_ANSI_RightBracket = Vk(code=30, name='kVK_ANSI_RightBracket', vsc=ScanCode(prefix=0, code=27))
kVK_ANSI_O = Vk(code=31, name='kVK_ANSI_O', vsc=ScanCode(prefix=0, code=24))
kVK_ANSI_U = Vk(code=32, name='kVK_ANSI_U', vsc=ScanCode(prefix=0, code=22))
kVK_ANSI_LeftBracket = Vk(code=33, name='kVK_ANSI_LeftBracket', vsc=ScanCode(prefix=0, code=26))
kVK_ANSI_I = Vk(code=34, name='kVK_ANSI_I', vsc=ScanCode(prefix=0, code=23))
kVK_ANSI_P = Vk(code=35, name='kVK_ANSI_P', vsc=ScanCode(prefix=0, code=25))
kVK_Return = Vk(code=36, name='kVK_Return', vsc=ScanCode(prefix=0, code=28))
kVK_ANSI_L = Vk(code=37, name='kVK_ANSI_L', vsc=ScanCode(prefix=0, code=38))
kVK_ANSI_J = Vk(code=38, name='kVK_ANSI_J', vsc=ScanCode(prefix=0, code=36))
kVK_ANSI_Quote = Vk(code=39, name='kVK_ANSI_Quote', vsc=ScanCode(prefix=0, code=40))
kVK_ANSI_K = Vk(code=40, name='kVK_ANSI_K', vsc=ScanCode(prefix=0, code=37))
kVK_ANSI_Semicolon = Vk(code=41, name='kVK_ANSI_Semicolon', vsc=ScanCode(prefix=0, code=39))
kVK_ANSI_Backslash = Vk(code=42, name='kVK_ANSI_Backslash', vsc=ScanCode(prefix=0, code=43))
kVK_ANSI_Comma = Vk(code=43, name='kVK_ANSI_Comma', vsc=ScanCode(prefix=0, code=51))
kVK_ANSI_Slash = Vk(code=44, name='kVK_ANSI_Slash', vsc=ScanCode(prefix=0, code=53))
kVK_ANSI_N = Vk(code=45, name='kVK_ANSI_N', vsc=ScanCode(prefix=0, code=49))
kVK_ANSI_M = Vk(code=46, name='kVK_ANSI_M', vsc=ScanCode(prefix=0, code=50))
kVK_ANSI_Period = Vk(code=47, name='kVK_ANSI_Period', vsc=ScanCode(prefix=0, code=52))
kVK_Tab = Vk(code=48, name='kVK_Tab', vsc=ScanCode(prefix=0, code=15))
kVK_Space = Vk(code=49, name='kVK_Space', vsc=ScanCode(prefix=0, code=57))
kVK_ANSI_Grave = Vk(code=50, name='kVK_ANSI_Grave', vsc=ScanCode(prefix=0, code=86))
kVK_Delete = Vk(code=51, name='kVK_Delete', vsc=ScanCode(prefix=0, code=14))
kVK_Escape = Vk(code=53, name='kVK_Escape', vsc=ScanCode(prefix=0, code=1))
kVK_Command = Vk(code=55, name='kVK_Command', vsc=ScanCode(prefix=224, code=91))
kVK_Shift = Vk(code=56, name='kVK_Shift', vsc=ScanCode(prefix=0, code=42))
kVK_CapsLock = Vk(code=57, name='kVK_CapsLock', vsc=ScanCode(prefix=0, code=58))
kVK_Option = Vk(code=58, name='kVK_Option', vsc=ScanCode(prefix=0, code=56))
kVK_Control = Vk(code=59, name='kVK_Control', vsc=ScanCode(prefix=0, code=29))
kVK_RightShift = Vk(code=60, name='kVK_RightShift', vsc=ScanCode(prefix=0, code=54))
kVK_RightOption = Vk(code=61, name='kVK_RightOption', vsc=ScanCode(prefix=224, code=56))
kVK_RightControl = Vk(code=62, name='kVK_RightControl', vsc=ScanCode(prefix=224, code=29))
kVK_ANSI_KeypadDecimal = Vk(code=65, name='kVK_ANSI_KeypadDecimal', vsc=ScanCode(prefix=0, code=83))
kVK_ANSI_KeypadMultiply = Vk(code=67, name='kVK_ANSI_KeypadMultiply', vsc=ScanCode(prefix=0, code=55))
kVK_ANSI_KeypadPlus = Vk(code=69, name='kVK_ANSI_KeypadPlus', vsc=ScanCode(prefix=0, code=78))
kVK_ANSI_KeypadClear = Vk(code=71, name='kVK_ANSI_KeypadClear', vsc=ScanCode(prefix=0, code=69))
kVK_VolumeUp = Vk(code=72, name='kVK_VolumeUp', vsc=ScanCode(prefix=224, code=48))
kVK_VolumeDown = Vk(code=73, name='kVK_VolumeDown', vsc=ScanCode(prefix=224, code=46))
kVK_Mute = Vk(code=74, name='kVK_Mute', vsc=ScanCode(prefix=224, code=32))
kVK_ANSI_KeypadDivide = Vk(code=75, name='kVK_ANSI_KeypadDivide', vsc=ScanCode(prefix=224, code=53))
kVK_ANSI_KeypadEnter = Vk(code=76, name='kVK_ANSI_KeypadEnter', vsc=ScanCode(prefix=224, code=28))
kVK_ANSI_KeypadMinus = Vk(code=78, name='kVK_ANSI_KeypadMinus', vsc=ScanCode(prefix=0, code=74))
kVK_ANSI_Keypad0 = Vk(code=82, name='kVK_ANSI_Keypad0', vsc=ScanCode(prefix=0, code=82))
kVK_ANSI_Keypad1 = Vk(code=83, name='kVK_ANSI_Keypad1', vsc=ScanCode(prefix=0, code=79))
kVK_ANSI_Keypad2 = Vk(code=84, name='kVK_ANSI_Keypad2', vsc=ScanCode(prefix=0, code=80))
kVK_ANSI_Keypad3 = Vk(code=85, name='kVK_ANSI_Keypad3', vsc=ScanCode(prefix=0, code=81))
kVK_ANSI_Keypad4 = Vk(code=86, name='kVK_ANSI_Keypad4', vsc=ScanCode(prefix=0, code=75))
kVK_ANSI_Keypad5 = Vk(code=87, name='kVK_ANSI_Keypad5', vsc=ScanCode(prefix=0, code=76))
kVK_ANSI_Keypad6 = Vk(code=88, name='kVK_ANSI_Keypad6', vsc=ScanCode(prefix=0, code=77))
kVK_ANSI_Keypad7 = Vk(code=89, name='kVK_ANSI_Keypad7', vsc=ScanCode(prefix=0, code=71))
kVK_ANSI_Keypad8 = Vk(code=91, name='kVK_ANSI_Keypad8', vsc=ScanCode(prefix=0, code=72))
kVK_ANSI_Keypad9 = Vk(code=92, name='kVK_ANSI_Keypad9', vsc=ScanCode(prefix=0, code=73))
kVK_F5 = Vk(code=96, name='kVK_F5', vsc=ScanCode(prefix=0, code=63))
kVK_F6 = Vk(code=97, name='kVK_F6', vsc=ScanCode(prefix=0, code=64))
kVK_F7 = Vk(code=98, name='kVK_F7', vsc=ScanCode(prefix=0, code=65))
kVK_F3 = Vk(code=99, name='kVK_F3', vsc=ScanCode(prefix=0, code=61))
kVK_F8 = Vk(code=100, name='kVK_F8', vsc=ScanCode(prefix=0, code=66))
kVK_F9 = Vk(code=101, name='kVK_F9', vsc=ScanCode(prefix=0, code=67))
kVK_F11 = Vk(code=103, name='kVK_F11', vsc=ScanCode(prefix=0, code=87))
kVK_F13 = Vk(code=105, name='kVK_F13', vsc=ScanCode(prefix=0, code=84))
kVK_F10 = Vk(code=109, name='kVK_F10', vsc=ScanCode(prefix=0, code=68))
kVK_F12 = Vk(code=111, name='kVK_F12', vsc=ScanCode(prefix=0, code=88))
kVK_Help = Vk(code=114, name='kVK_Help', vsc=ScanCode(prefix=224, code=82))
kVK_Home = Vk(code=115, name='kVK_Home', vsc=ScanCode(prefix=224, code=71))
kVK_PageUp = Vk(code=116, name='kVK_PageUp', vsc=ScanCode(prefix=224, code=73))
kVK_ForwardDelete = Vk(code=117, name='kVK_ForwardDelete', vsc=ScanCode(prefix=224, code=83))
kVK_F4 = Vk(code=118, name='kVK_F4', vsc=ScanCode(prefix=0, code=62))
kVK_End = Vk(code=119, name='kVK_End', vsc=ScanCode(prefix=224, code=79))
kVK_F2 = Vk(code=120, name='kVK_F2', vsc=ScanCode(prefix=0, code=60))
kVK_PageDown = Vk(code=121, name='kVK_PageDown', vsc=ScanCode(prefix=224, code=81))
kVK_F1 = Vk(code=122, name='kVK_F1', vsc=ScanCode(prefix=0, code=59))
kVK_LeftArrow = Vk(code=123, name='kVK_LeftArrow', vsc=ScanCode(prefix=224, code=75))
kVK_RightArrow = Vk(code=124, name='kVK_RightArrow', vsc=ScanCode(prefix=224, code=77))
kVK_DownArrow = Vk(code=125, name='kVK_DownArrow', vsc=ScanCode(prefix=224, code=80))
kVK_UpArrow = Vk(code=126, name='kVK_UpArrow', vsc=ScanCode(prefix=224, code=72))

all = [
    kVK_ANSI_A,
    kVK_ANSI_S,
    kVK_ANSI_D,
    kVK_ANSI_F,
    kVK_ANSI_H,
    kVK_ANSI_G,
    kVK_ANSI_Z,
    kVK_ANSI_X,
    kVK_ANSI_C,
    kVK_ANSI_V,
    kVK_ISO_Section,
    kVK_ANSI_B,
    kVK_ANSI_Q,
    kVK_ANSI_W,
    kVK_ANSI_E,
    kVK_ANSI_R,
    kVK_ANSI_Y,
    kVK_ANSI_T,
    kVK_ANSI_1,
    kVK_ANSI_2,
    kVK_ANSI_3,
    kVK_ANSI_4,
    kVK_ANSI_6,
    kVK_ANSI_5,
    kVK_ANSI_Equal,
    kVK_ANSI_9,
    kVK_ANSI_7,
    kVK_ANSI_Minus,
    kVK_ANSI_8,
    kVK_ANSI_0,
    kVK_ANSI_RightBracket,
    kVK_ANSI_O,
    kVK_ANSI_U,
    kVK_ANSI_LeftBracket,
    kVK_ANSI_I,
    kVK_ANSI_P,
    kVK_Return,
    kVK_ANSI_L,
    kVK_ANSI_J,
    kVK_ANSI_Quote,
    kVK_ANSI_K,
    kVK_ANSI_Semicolon,
    kVK_ANSI_Backslash,
    kVK_ANSI_Comma,
    kVK_ANSI_Slash,
    kVK_ANSI_N,
    kVK_ANSI_M,
    kVK_ANSI_Period,
    kVK_Tab,
    kVK_Space,
    kVK_ANSI_Grave,
    kVK_Delete,
    kVK_Escape,
    kVK_Command,
    kVK_Shift,
    kVK_CapsLock,
    kVK_Option,
    kVK_Control,
    kVK_RightShift,
    kVK_RightOption,
    kVK_RightControl,
    kVK_ANSI_KeypadDecimal,
    kVK_ANSI_KeypadMultiply,
    kVK_ANSI_KeypadPlus,
    kVK_ANSI_KeypadClear,
    kVK_VolumeUp,
    kVK_VolumeDown,
    kVK_Mute,
    kVK_ANSI_KeypadDivide,
    kVK_ANSI_KeypadEnter,
    kVK_ANSI_KeypadMinus,
    kVK_ANSI_Keypad0,
    kVK_ANSI_Keypad1,
    kVK_ANSI_Keypad2,
    kVK_ANSI_Keypad3,
    kVK_ANSI_Keypad4,
    kVK_ANSI_Keypad5,
    kVK_ANSI_Keypad6,
    kVK_ANSI_Keypad7,
    kVK_ANSI_Keypad8,
    kVK_ANSI_Keypad9,
    kVK_F5,
    kVK_F6,
    kVK_F7,
    kVK_F3,
    kVK_F8,
    kVK_F9,
    kVK_F11,
    kVK_F13,
    kVK_F10,
    kVK_F12,
    kVK_Help,
    kVK_Home,
    kVK_PageUp,
    kVK_ForwardDelete,
    kVK_F4,
    kVK_End,
    kVK_F2,
    kVK_PageDown,
    kVK_F1,
    kVK_LeftArrow,
    kVK_RightArrow,
    kVK_DownArrow,
    kVK_UpArrow,
]

vsc_to_vk = {
    ScanCode(prefix=0, code=1): kVK_Escape,
    ScanCode(prefix=0, code=2): kVK_ANSI_1,
    ScanCode(prefix=0, code=3): kVK_ANSI_2,
    ScanCode(prefix=0, code=4): kVK_ANSI_3,
    ScanCode(prefix=0, code=5): kVK_ANSI_4,
    ScanCode(prefix=0, code=6): kVK_ANSI_5,
    ScanCode(prefix=0, code=7): kVK_ANSI_6,
    ScanCode(prefix=0, code=8): kVK_ANSI_7,
    ScanCode(prefix=0, code=9): kVK_ANSI_8,
    ScanCode(prefix=0, code=10): kVK_ANSI_9,
    ScanCode(prefix=0, code=11): kVK_ANSI_0,
    ScanCode(prefix=0, code=12): kVK_ANSI_Minus,
    ScanCode(prefix=0, code=13): kVK_ANSI_Equal,
    ScanCode(prefix=0, code=14): kVK_Delete,
    ScanCode(prefix=0, code=15): kVK_Tab,
    ScanCode(prefix=0, code=16): kVK_ANSI_Q,
    ScanCode(prefix=0, code=17): kVK_ANSI_W,
    ScanCode(prefix=0, code=18): kVK_ANSI_E,
    ScanCode(prefix=0, code=19): kVK_ANSI_R,
    ScanCode(prefix=0, code=20): kVK_ANSI_T,
    ScanCode(prefix=0, code=21): kVK_ANSI_Y,
    ScanCode(prefix=0, code=22): kVK_ANSI_U,
    ScanCode(prefix=0, code=23): kVK_ANSI_I,
    ScanCode(prefix=0, code=24): kVK_ANSI_O,
    ScanCode(prefix=0, code=25): kVK_ANSI_P,
    ScanCode(prefix=0, code=26): kVK_ANSI_LeftBracket,
    ScanCode(prefix=0, code=27): kVK_ANSI_RightBracket,
    ScanCode(prefix=0, code=28): kVK_Return,
    ScanCode(prefix=0, code=29): kVK_Control,
    ScanCode(prefix=0, code=30): kVK_ANSI_A,
    ScanCode(prefix=0, code=31): kVK_ANSI_S,
    ScanCode(prefix=0, code=32): kVK_ANSI_D,
    ScanCode(prefix=0, code=33): kVK_ANSI_F,
    ScanCode(prefix=0, code=34): kVK_ANSI_G,
    ScanCode(prefix=0, code=35): kVK_ANSI_H,
    ScanCode(prefix=0, code=36): kVK_ANSI_J,
    ScanCode(prefix=0, code=37): kVK_ANSI_K,
    ScanCode(prefix=0, code=38): kVK_ANSI_L,
    ScanCode(prefix=0, code=39): kVK_ANSI_Semicolon,
    ScanCode(prefix=0, code=40): kVK_ANSI_Quote,
    ScanCode(prefix=0, code=41): kVK_ISO_Section,
    ScanCode(prefix=0, code=42): kVK_Shift,
    ScanCode(prefix=0, code=43): kVK_ANSI_Backslash,
    ScanCode(prefix=0, code=44): kVK_ANSI_Z,
    ScanCode(prefix=0, code=45): kVK_ANSI_X,
    ScanCode(prefix=0, code=46): kVK_ANSI_C,
    ScanCode(prefix=0, code=47): kVK_ANSI_V,
    ScanCode(prefix=0, code=48): kVK_ANSI_B,
    ScanCode(prefix=0, code=49): kVK_ANSI_N,
    ScanCode(prefix=0, code=50): kVK_ANSI_M,
    ScanCode(prefix=0, code=51): kVK_ANSI_Comma,
    ScanCode(prefix=0, code=52): kVK_ANSI_Period,
    ScanCode(prefix=0, code=53): kVK_ANSI_Slash,
    ScanCode(prefix=0, code=54): kVK_RightShift,
    ScanCode(prefix=0, code=55): kVK_ANSI_KeypadMultiply,
    ScanCode(prefix=0, code=56): kVK_Option,
    ScanCode(prefix=0, code=57): kVK_Space,
    ScanCode(prefix=0, code=58): kVK_CapsLock,
    ScanCode(prefix=0, code=59): kVK_F1,
    ScanCode(prefix=0, code=60): kVK_F2,
    ScanCode(prefix=0, code=61): kVK_F3,
    ScanCode(prefix=0, code=62): kVK_F4,
    ScanCode(prefix=0, code=63): kVK_F5,
    ScanCode(prefix=0, code=64): kVK_F6,
    ScanCode(prefix=0, code=65): kVK_F7,
    ScanCode(prefix=0, code=66): kVK_F8,
    ScanCode(prefix=0, code=67): kVK_F9,
    ScanCode(prefix=0, code=68): kVK_F10,
    ScanCode(prefix=0, code=69): kVK_ANSI_KeypadClear,
    ScanCode(prefix=0, code=71): kVK_ANSI_Keypad7,
    ScanCode(prefix=0, code=72): kVK_ANSI_Keypad8,
    ScanCode(prefix=0, code=73): kVK_ANSI_Keypad9,
    ScanCode(prefix=0, code=74): kVK_ANSI_KeypadMinus,
    ScanCode(prefix=0, code=75): kVK_ANSI_Keypad4,
    ScanCode(prefix=0, code=76): kVK_ANSI_Keypad5,
    ScanCode(prefix=0, code=77): kVK_ANSI_Keypad6,
    ScanCode(prefix=0, code=78): kVK_ANSI_KeypadPlus,
    ScanCode(prefix=0, code=79): kVK_ANSI_Keypad1,
    ScanCode(prefix=0, code=80): kVK_ANSI_Keypad2,
    ScanCode(prefix=0, code=81): kVK_ANSI_Keypad3,
    ScanCode(prefix=0, code=82): kVK_ANSI_Keypad0,
    ScanCode(prefix=0, code=83): kVK_ANSI_KeypadDecimal,
    ScanCode(prefix=0, code=84): kVK_F13,
    ScanCode(prefix=0, code=86): kVK_ANSI_Grave,
    ScanCode(prefix=0, code=87): kVK_F11,
    ScanCode(prefix=0, code=88): kVK_F12,
    ScanCode(prefix=224, code=28): kVK_ANSI_KeypadEnter,
    ScanCode(prefix=224, code=29): kVK_RightControl,
    ScanCode(prefix=224, code=32): kVK_Mute,
    ScanCode(prefix=224, code=46): kVK_VolumeDown,
    ScanCode(prefix=224, code=48): kVK_VolumeUp,
    ScanCode(prefix=224, code=53): kVK_ANSI_KeypadDivide,
    ScanCode(prefix=224, code=56): kVK_RightOption,
    ScanCode(prefix=224, code=71): kVK_Home,
    ScanCode(prefix=224, code=72): kVK_UpArrow,
    ScanCode(prefix=224, code=73): kVK_PageUp,
    ScanCode(prefix=224, code=75): kVK_LeftArrow,
    ScanCode(prefix=224, code=77): kVK_RightArrow,
    ScanCode(prefix=224, code=79): kVK_End,
    ScanCode(prefix=224, code=80): kVK_DownArrow,
    ScanCode(prefix=224, code=81): kVK_PageDown,
    ScanCode(prefix=224, code=82): kVK_Help,
    ScanCode(prefix=224, code=83): kVK_ForwardDelete,
    ScanCode(prefix=224, code=91): kVK_Command,
}
