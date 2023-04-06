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
