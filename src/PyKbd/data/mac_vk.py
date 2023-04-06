from dataclasses import dataclass


@dataclass(frozen=True)
class Vk:
    code: int
    name: str
    vsc: int  # used to lookup win_vk for current layout


def _generate(f):
    ansi = [
        Vk(0x00, "kVK_ANSI_A", 0x1E),
        Vk(0x01, "kVK_ANSI_S", 0x1F),
        Vk(0x02, "kVK_ANSI_D", 0x20),
        Vk(0x03, "kVK_ANSI_F", 0x21),
        Vk(0x04, "kVK_ANSI_H", 0x23),
        Vk(0x05, "kVK_ANSI_G", 0x22),
        Vk(0x06, "kVK_ANSI_Z", 0x2C),
        Vk(0x07, "kVK_ANSI_X", 0x2D),
        Vk(0x08, "kVK_ANSI_C", 0x2E),
        Vk(0x09, "kVK_ANSI_V", 0x2F),
        Vk(0x0B, "kVK_ANSI_B", 0x30),
        Vk(0x0C, "kVK_ANSI_Q", 0x10),
        Vk(0x0D, "kVK_ANSI_W", 0x11),
        Vk(0x0E, "kVK_ANSI_E", 0x12),
        Vk(0x0F, "kVK_ANSI_R", 0x13),
        Vk(0x10, "kVK_ANSI_Y", 0x15),
        Vk(0x11, "kVK_ANSI_T", 0x14),
        Vk(0x12, "kVK_ANSI_1", 0x02),
        Vk(0x13, "kVK_ANSI_2", 0x03),
        Vk(0x14, "kVK_ANSI_3", 0x04),
        Vk(0x15, "kVK_ANSI_4", 0x05),
        Vk(0x16, "kVK_ANSI_6", 0x07),
        Vk(0x17, "kVK_ANSI_5", 0x06),
        Vk(0x18, "kVK_ANSI_Equal", 0x0D),
        Vk(0x19, "kVK_ANSI_9", 0x0A),
        Vk(0x1A, "kVK_ANSI_7", 0x08),
        Vk(0x1B, "kVK_ANSI_Minus", 0x0C),
        Vk(0x1C, "kVK_ANSI_8", 0x09),
        Vk(0x1D, "kVK_ANSI_0", 0x0B),
        Vk(0x1E, "kVK_ANSI_RightBracket", 0x1B),
        Vk(0x1F, "kVK_ANSI_O", 0x18),
        Vk(0x20, "kVK_ANSI_U", 0x16),
        Vk(0x21, "kVK_ANSI_LeftBracket", 0x1A),
        Vk(0x22, "kVK_ANSI_I", 0x17),
        Vk(0x23, "kVK_ANSI_P", 0x19),
        Vk(0x25, "kVK_ANSI_L", 0x26),
        Vk(0x26, "kVK_ANSI_J", 0x24),
        Vk(0x27, "kVK_ANSI_Quote", 0x28),
        Vk(0x28, "kVK_ANSI_K", 0x25),
        Vk(0x29, "kVK_ANSI_Semicolon", 0x27),
        Vk(0x2A, "kVK_ANSI_Backslash", 0x2B),
        Vk(0x2B, "kVK_ANSI_Comma", 0x33),
        Vk(0x2C, "kVK_ANSI_Slash", 0x35),
        Vk(0x2D, "kVK_ANSI_N", 0x31),
        Vk(0x2E, "kVK_ANSI_M", 0x32),
        Vk(0x2F, "kVK_ANSI_Period", 0x34),
        Vk(0x32, "kVK_ANSI_Grave", 0x29),
        Vk(0x41, "kVK_ANSI_KeypadDecimal", 0x53),
        Vk(0x43, "kVK_ANSI_KeypadMultiply", 0x37),
        Vk(0x45, "kVK_ANSI_KeypadPlus", 0x4E),
        #Vk(0x47, "kVK_ANSI_KeypadClear", 0x00),  # TODO ???
        Vk(0x4B, "kVK_ANSI_KeypadDivide", 0xE035),
        Vk(0x4C, "kVK_ANSI_KeypadEnter", 0xE01C),
        Vk(0x4E, "kVK_ANSI_KeypadMinus", 0x4A),
        #Vk(0x51, "kVK_ANSI_KeypadEquals", 0x00),  # TODO ???
        Vk(0x52, "kVK_ANSI_Keypad0", 0x52),
        Vk(0x53, "kVK_ANSI_Keypad1", 0x4F),
        Vk(0x54, "kVK_ANSI_Keypad2", 0x50),
        Vk(0x55, "kVK_ANSI_Keypad3", 0x51),
        Vk(0x56, "kVK_ANSI_Keypad4", 0x4B),
        Vk(0x57, "kVK_ANSI_Keypad5", 0x4C),
        Vk(0x58, "kVK_ANSI_Keypad6", 0x4D),
        Vk(0x59, "kVK_ANSI_Keypad7", 0x47),
        Vk(0x5B, "kVK_ANSI_Keypad8", 0x48),
        Vk(0x5C, "kVK_ANSI_Keypad9", 0x49),
    ]

    general = [
        Vk(0x24, "kVK_Return", 0x1C),
        Vk(0x30, "kVK_Tab", 0x0F),
        Vk(0x31, "kVK_Space", 0x39),
        Vk(0x33, "kVK_Delete", 0xE04B),
        Vk(0x35, "kVK_Escape", 0x01),
        Vk(0x37, "kVK_Command", 0xE05B),
        Vk(0x38, "kVK_Shift", 0x2A),
        Vk(0x39, "kVK_CapsLock", 0x3A),
        Vk(0x3A, "kVK_Option", 0x38),
        Vk(0x3B, "kVK_Control", 0x1D),
        Vk(0x3C, "kVK_RightShift", 0x36),
        Vk(0x3D, "kVK_RightOption", 0xE038),
        Vk(0x3E, "kVK_RightControl", 0xE01D),
        #Vk(0x3F, "kVK_Function", 0x00),  # TODO ??
        #Vk(0x40, "kVK_F17", 0x00),  # TODO ??
        #Vk(0x48, "kVK_VolumeUp", 0x00),  # TODO ??
        #Vk(0x49, "kVK_VolumeDown", 0x00),  # TODO ??
        #Vk(0x4A, "kVK_Mute", 0x00),  # TODO ??
        #Vk(0x4F, "kVK_F18", 0x00),  # TODO ??
        #Vk(0x50, "kVK_F19", 0x00),  # TODO ??
        #Vk(0x5A, "kVK_F20", 0x00),  # TODO ??
        Vk(0x60, "kVK_F5", 0x3F),
        Vk(0x61, "kVK_F6", 0x40),
        Vk(0x62, "kVK_F7", 0X41),
        Vk(0x63, "kVK_F3", 0x3D),
        Vk(0x64, "kVK_F8", 0x42),
        Vk(0x65, "kVK_F9", 0x43),
        Vk(0x67, "kVK_F11", 0x57),
        #Vk(0x69, "kVK_F13", 0x00),  # TODO ??
        #Vk(0x6A, "kVK_F16", 0x00),  # TODO ??
        #Vk(0x6B, "kVK_F14", 0x00),  # TODO ??
        Vk(0x6D, "kVK_F10", 0x44),
        Vk(0x6F, "kVK_F12", 0x58),
        #Vk(0x71, "kVK_F15", 0x00),  # TODO ??
        Vk(0x72, "kVK_Help", 0xE052),
        Vk(0x73, "kVK_Home", 0xE047),
        Vk(0x74, "kVK_PageUp", 0xE049),
        #Vk(0x75, "kVK_ForwardDelete", 0x00),  # TODO ??
        Vk(0x76, "kVK_F4", 0x3E),
        Vk(0x77, "kVK_End", 0xE04F),
        Vk(0x78, "kVK_F2", 0x3C),
        Vk(0x79, "kVK_PageDown", 0xE051),
        Vk(0x7A, "kVK_F1", 0x3B),
        Vk(0x7B, "kVK_LeftArrow", 0xE04B),
        Vk(0x7C, "kVK_RightArrow", 0xE04D),
        Vk(0x7D, "kVK_DownArrow", 0xE050),
        Vk(0x7E, "kVK_UpArrow", 0xE048),
    ]

    iso = [
        Vk(0x0A, "kVK_ISO_Section", 0x56),
    ]

    #jis = [
    #    Vk(0x5D, "kVK_JIS_Yen", 0x0),  # TODO, T7D -> OEM_5?
    #    Vk(0x5E, "kVK_JIS_Underscore", 0x0),  # TODO ??
    #    Vk(0x5F, "kVK_JIS_KeypadComma", 0x0),  # TODO ??
    #    Vk(0x66, "kVK_JIS_Eisu", 0x0),  # TODO ??
    #    Vk(0x68, "kVK_JIS_Kana", 0x0),  # TODO ??
    #]

    all = [*ansi, *general, *iso]

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
            with open(__file__, "r", encoding="ascii", errors="strict") as s:
                f.write(s.read())
            print(file=f)
            _generate(f)

    _main()

# ----- start generated content -----

kVK_ANSI_A = Vk(code=0, name='kVK_ANSI_A', vsc=30)
kVK_ANSI_S = Vk(code=1, name='kVK_ANSI_S', vsc=31)
kVK_ANSI_D = Vk(code=2, name='kVK_ANSI_D', vsc=32)
kVK_ANSI_F = Vk(code=3, name='kVK_ANSI_F', vsc=33)
kVK_ANSI_H = Vk(code=4, name='kVK_ANSI_H', vsc=35)
kVK_ANSI_G = Vk(code=5, name='kVK_ANSI_G', vsc=34)
kVK_ANSI_Z = Vk(code=6, name='kVK_ANSI_Z', vsc=44)
kVK_ANSI_X = Vk(code=7, name='kVK_ANSI_X', vsc=45)
kVK_ANSI_C = Vk(code=8, name='kVK_ANSI_C', vsc=46)
kVK_ANSI_V = Vk(code=9, name='kVK_ANSI_V', vsc=47)
kVK_ANSI_B = Vk(code=11, name='kVK_ANSI_B', vsc=48)
kVK_ANSI_Q = Vk(code=12, name='kVK_ANSI_Q', vsc=16)
kVK_ANSI_W = Vk(code=13, name='kVK_ANSI_W', vsc=17)
kVK_ANSI_E = Vk(code=14, name='kVK_ANSI_E', vsc=18)
kVK_ANSI_R = Vk(code=15, name='kVK_ANSI_R', vsc=19)
kVK_ANSI_Y = Vk(code=16, name='kVK_ANSI_Y', vsc=21)
kVK_ANSI_T = Vk(code=17, name='kVK_ANSI_T', vsc=20)
kVK_ANSI_1 = Vk(code=18, name='kVK_ANSI_1', vsc=2)
kVK_ANSI_2 = Vk(code=19, name='kVK_ANSI_2', vsc=3)
kVK_ANSI_3 = Vk(code=20, name='kVK_ANSI_3', vsc=4)
kVK_ANSI_4 = Vk(code=21, name='kVK_ANSI_4', vsc=5)
kVK_ANSI_6 = Vk(code=22, name='kVK_ANSI_6', vsc=7)
kVK_ANSI_5 = Vk(code=23, name='kVK_ANSI_5', vsc=6)
kVK_ANSI_Equal = Vk(code=24, name='kVK_ANSI_Equal', vsc=13)
kVK_ANSI_9 = Vk(code=25, name='kVK_ANSI_9', vsc=10)
kVK_ANSI_7 = Vk(code=26, name='kVK_ANSI_7', vsc=8)
kVK_ANSI_Minus = Vk(code=27, name='kVK_ANSI_Minus', vsc=12)
kVK_ANSI_8 = Vk(code=28, name='kVK_ANSI_8', vsc=9)
kVK_ANSI_0 = Vk(code=29, name='kVK_ANSI_0', vsc=11)
kVK_ANSI_RightBracket = Vk(code=30, name='kVK_ANSI_RightBracket', vsc=27)
kVK_ANSI_O = Vk(code=31, name='kVK_ANSI_O', vsc=24)
kVK_ANSI_U = Vk(code=32, name='kVK_ANSI_U', vsc=22)
kVK_ANSI_LeftBracket = Vk(code=33, name='kVK_ANSI_LeftBracket', vsc=26)
kVK_ANSI_I = Vk(code=34, name='kVK_ANSI_I', vsc=23)
kVK_ANSI_P = Vk(code=35, name='kVK_ANSI_P', vsc=25)
kVK_ANSI_L = Vk(code=37, name='kVK_ANSI_L', vsc=38)
kVK_ANSI_J = Vk(code=38, name='kVK_ANSI_J', vsc=36)
kVK_ANSI_Quote = Vk(code=39, name='kVK_ANSI_Quote', vsc=40)
kVK_ANSI_K = Vk(code=40, name='kVK_ANSI_K', vsc=37)
kVK_ANSI_Semicolon = Vk(code=41, name='kVK_ANSI_Semicolon', vsc=39)
kVK_ANSI_Backslash = Vk(code=42, name='kVK_ANSI_Backslash', vsc=43)
kVK_ANSI_Comma = Vk(code=43, name='kVK_ANSI_Comma', vsc=51)
kVK_ANSI_Slash = Vk(code=44, name='kVK_ANSI_Slash', vsc=53)
kVK_ANSI_N = Vk(code=45, name='kVK_ANSI_N', vsc=49)
kVK_ANSI_M = Vk(code=46, name='kVK_ANSI_M', vsc=50)
kVK_ANSI_Period = Vk(code=47, name='kVK_ANSI_Period', vsc=52)
kVK_ANSI_Grave = Vk(code=50, name='kVK_ANSI_Grave', vsc=41)
kVK_ANSI_KeypadDecimal = Vk(code=65, name='kVK_ANSI_KeypadDecimal', vsc=83)
kVK_ANSI_KeypadMultiply = Vk(code=67, name='kVK_ANSI_KeypadMultiply', vsc=55)
kVK_ANSI_KeypadPlus = Vk(code=69, name='kVK_ANSI_KeypadPlus', vsc=78)
kVK_ANSI_KeypadDivide = Vk(code=75, name='kVK_ANSI_KeypadDivide', vsc=57397)
kVK_ANSI_KeypadEnter = Vk(code=76, name='kVK_ANSI_KeypadEnter', vsc=57372)
kVK_ANSI_KeypadMinus = Vk(code=78, name='kVK_ANSI_KeypadMinus', vsc=74)
kVK_ANSI_Keypad0 = Vk(code=82, name='kVK_ANSI_Keypad0', vsc=82)
kVK_ANSI_Keypad1 = Vk(code=83, name='kVK_ANSI_Keypad1', vsc=79)
kVK_ANSI_Keypad2 = Vk(code=84, name='kVK_ANSI_Keypad2', vsc=80)
kVK_ANSI_Keypad3 = Vk(code=85, name='kVK_ANSI_Keypad3', vsc=81)
kVK_ANSI_Keypad4 = Vk(code=86, name='kVK_ANSI_Keypad4', vsc=75)
kVK_ANSI_Keypad5 = Vk(code=87, name='kVK_ANSI_Keypad5', vsc=76)
kVK_ANSI_Keypad6 = Vk(code=88, name='kVK_ANSI_Keypad6', vsc=77)
kVK_ANSI_Keypad7 = Vk(code=89, name='kVK_ANSI_Keypad7', vsc=71)
kVK_ANSI_Keypad8 = Vk(code=91, name='kVK_ANSI_Keypad8', vsc=72)
kVK_ANSI_Keypad9 = Vk(code=92, name='kVK_ANSI_Keypad9', vsc=73)
kVK_Return = Vk(code=36, name='kVK_Return', vsc=28)
kVK_Tab = Vk(code=48, name='kVK_Tab', vsc=15)
kVK_Space = Vk(code=49, name='kVK_Space', vsc=57)
kVK_Delete = Vk(code=51, name='kVK_Delete', vsc=57419)
kVK_Escape = Vk(code=53, name='kVK_Escape', vsc=1)
kVK_Command = Vk(code=55, name='kVK_Command', vsc=57435)
kVK_Shift = Vk(code=56, name='kVK_Shift', vsc=42)
kVK_CapsLock = Vk(code=57, name='kVK_CapsLock', vsc=58)
kVK_Option = Vk(code=58, name='kVK_Option', vsc=56)
kVK_Control = Vk(code=59, name='kVK_Control', vsc=29)
kVK_RightShift = Vk(code=60, name='kVK_RightShift', vsc=54)
kVK_RightOption = Vk(code=61, name='kVK_RightOption', vsc=57400)
kVK_RightControl = Vk(code=62, name='kVK_RightControl', vsc=57373)
kVK_F5 = Vk(code=96, name='kVK_F5', vsc=63)
kVK_F6 = Vk(code=97, name='kVK_F6', vsc=64)
kVK_F7 = Vk(code=98, name='kVK_F7', vsc=65)
kVK_F3 = Vk(code=99, name='kVK_F3', vsc=61)
kVK_F8 = Vk(code=100, name='kVK_F8', vsc=66)
kVK_F9 = Vk(code=101, name='kVK_F9', vsc=67)
kVK_F11 = Vk(code=103, name='kVK_F11', vsc=87)
kVK_F10 = Vk(code=109, name='kVK_F10', vsc=68)
kVK_F12 = Vk(code=111, name='kVK_F12', vsc=88)
kVK_Help = Vk(code=114, name='kVK_Help', vsc=57426)
kVK_Home = Vk(code=115, name='kVK_Home', vsc=57415)
kVK_PageUp = Vk(code=116, name='kVK_PageUp', vsc=57417)
kVK_F4 = Vk(code=118, name='kVK_F4', vsc=62)
kVK_End = Vk(code=119, name='kVK_End', vsc=57423)
kVK_F2 = Vk(code=120, name='kVK_F2', vsc=60)
kVK_PageDown = Vk(code=121, name='kVK_PageDown', vsc=57425)
kVK_F1 = Vk(code=122, name='kVK_F1', vsc=59)
kVK_LeftArrow = Vk(code=123, name='kVK_LeftArrow', vsc=57419)
kVK_RightArrow = Vk(code=124, name='kVK_RightArrow', vsc=57421)
kVK_DownArrow = Vk(code=125, name='kVK_DownArrow', vsc=57424)
kVK_UpArrow = Vk(code=126, name='kVK_UpArrow', vsc=57416)
kVK_ISO_Section = Vk(code=10, name='kVK_ISO_Section', vsc=86)

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
    kVK_ANSI_Grave,
    kVK_ANSI_KeypadDecimal,
    kVK_ANSI_KeypadMultiply,
    kVK_ANSI_KeypadPlus,
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
    kVK_Return,
    kVK_Tab,
    kVK_Space,
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
    kVK_F5,
    kVK_F6,
    kVK_F7,
    kVK_F3,
    kVK_F8,
    kVK_F9,
    kVK_F11,
    kVK_F10,
    kVK_F12,
    kVK_Help,
    kVK_Home,
    kVK_PageUp,
    kVK_F4,
    kVK_End,
    kVK_F2,
    kVK_PageDown,
    kVK_F1,
    kVK_LeftArrow,
    kVK_RightArrow,
    kVK_DownArrow,
    kVK_UpArrow,
    kVK_ISO_Section,
]

vsc_to_vk = {
    1: kVK_Escape,
    2: kVK_ANSI_1,
    3: kVK_ANSI_2,
    4: kVK_ANSI_3,
    5: kVK_ANSI_4,
    6: kVK_ANSI_5,
    7: kVK_ANSI_6,
    8: kVK_ANSI_7,
    9: kVK_ANSI_8,
    10: kVK_ANSI_9,
    11: kVK_ANSI_0,
    12: kVK_ANSI_Minus,
    13: kVK_ANSI_Equal,
    15: kVK_Tab,
    16: kVK_ANSI_Q,
    17: kVK_ANSI_W,
    18: kVK_ANSI_E,
    19: kVK_ANSI_R,
    20: kVK_ANSI_T,
    21: kVK_ANSI_Y,
    22: kVK_ANSI_U,
    23: kVK_ANSI_I,
    24: kVK_ANSI_O,
    25: kVK_ANSI_P,
    26: kVK_ANSI_LeftBracket,
    27: kVK_ANSI_RightBracket,
    28: kVK_Return,
    29: kVK_Control,
    30: kVK_ANSI_A,
    31: kVK_ANSI_S,
    32: kVK_ANSI_D,
    33: kVK_ANSI_F,
    34: kVK_ANSI_G,
    35: kVK_ANSI_H,
    36: kVK_ANSI_J,
    37: kVK_ANSI_K,
    38: kVK_ANSI_L,
    39: kVK_ANSI_Semicolon,
    40: kVK_ANSI_Quote,
    41: kVK_ANSI_Grave,
    42: kVK_Shift,
    43: kVK_ANSI_Backslash,
    44: kVK_ANSI_Z,
    45: kVK_ANSI_X,
    46: kVK_ANSI_C,
    47: kVK_ANSI_V,
    48: kVK_ANSI_B,
    49: kVK_ANSI_N,
    50: kVK_ANSI_M,
    51: kVK_ANSI_Comma,
    52: kVK_ANSI_Period,
    53: kVK_ANSI_Slash,
    54: kVK_RightShift,
    55: kVK_ANSI_KeypadMultiply,
    56: kVK_Option,
    57: kVK_Space,
    58: kVK_CapsLock,
    59: kVK_F1,
    60: kVK_F2,
    61: kVK_F3,
    62: kVK_F4,
    63: kVK_F5,
    64: kVK_F6,
    65: kVK_F7,
    66: kVK_F8,
    67: kVK_F9,
    68: kVK_F10,
    71: kVK_ANSI_Keypad7,
    72: kVK_ANSI_Keypad8,
    73: kVK_ANSI_Keypad9,
    74: kVK_ANSI_KeypadMinus,
    75: kVK_ANSI_Keypad4,
    76: kVK_ANSI_Keypad5,
    77: kVK_ANSI_Keypad6,
    78: kVK_ANSI_KeypadPlus,
    79: kVK_ANSI_Keypad1,
    80: kVK_ANSI_Keypad2,
    81: kVK_ANSI_Keypad3,
    82: kVK_ANSI_Keypad0,
    83: kVK_ANSI_KeypadDecimal,
    86: kVK_ISO_Section,
    87: kVK_F11,
    88: kVK_F12,
    57372: kVK_ANSI_KeypadEnter,
    57373: kVK_RightControl,
    57397: kVK_ANSI_KeypadDivide,
    57400: kVK_RightOption,
    57415: kVK_Home,
    57416: kVK_UpArrow,
    57417: kVK_PageUp,
    57419: kVK_LeftArrow,
    57421: kVK_RightArrow,
    57423: kVK_End,
    57424: kVK_DownArrow,
    57425: kVK_PageDown,
    57426: kVK_Help,
    57435: kVK_Command,
}
