from dataclasses import dataclass

from PyKbd.layout import ScanCode


@dataclass(frozen=True)
class KeyCode:
    code: int
    name: str
    vsc: ScanCode


def _generate(f):
    xfree86 = [
        KeyCode(49, "TLDE", ScanCode(0x29)),
        # KeyCode(49, "AE00", ScanCode(0x29)),
        KeyCode(10, "AE01", ScanCode(0x02)),
        KeyCode(11, "AE02", ScanCode(0x03)),
        KeyCode(12, "AE03", ScanCode(0x04)),
        KeyCode(13, "AE04", ScanCode(0x05)),
        KeyCode(14, "AE05", ScanCode(0x06)),
        KeyCode(15, "AE06", ScanCode(0x07)),
        KeyCode(16, "AE07", ScanCode(0x08)),
        KeyCode(17, "AE08", ScanCode(0x09)),
        KeyCode(18, "AE09", ScanCode(0x0A)),
        KeyCode(19, "AE10", ScanCode(0x0B)),
        KeyCode(20, "AE11", ScanCode(0x0C)),
        KeyCode(21, "AE12", ScanCode(0x0D)),
        KeyCode(22, "BKSP", ScanCode(0x0E)),

        KeyCode(23, "TAB", ScanCode(0x0F)),
        KeyCode(24, "AD01", ScanCode(0x10)),
        KeyCode(25, "AD02", ScanCode(0x11)),
        KeyCode(26, "AD03", ScanCode(0x12)),
        KeyCode(27, "AD04", ScanCode(0x13)),
        KeyCode(28, "AD05", ScanCode(0x14)),
        KeyCode(29, "AD06", ScanCode(0x15)),
        KeyCode(30, "AD07", ScanCode(0x16)),
        KeyCode(31, "AD08", ScanCode(0x17)),
        KeyCode(32, "AD09", ScanCode(0x18)),
        KeyCode(33, "AD10", ScanCode(0x19)),
        KeyCode(34, "AD11", ScanCode(0x1A)),
        KeyCode(35, "AD12", ScanCode(0x1B)),
        KeyCode(36, "RTRN", ScanCode(0x1C)),

        KeyCode(66, "CAPS", ScanCode(0x3A)),
        KeyCode(38, "AC01", ScanCode(0x1E)),
        KeyCode(39, "AC02", ScanCode(0x1F)),
        KeyCode(40, "AC03", ScanCode(0x20)),
        KeyCode(41, "AC04", ScanCode(0x21)),
        KeyCode(42, "AC05", ScanCode(0x22)),
        KeyCode(43, "AC06", ScanCode(0x23)),
        KeyCode(44, "AC07", ScanCode(0x24)),
        KeyCode(45, "AC08", ScanCode(0x25)),
        KeyCode(46, "AC09", ScanCode(0x26)),
        KeyCode(47, "AC10", ScanCode(0x27)),
        KeyCode(48, "AC11", ScanCode(0x28)),
        KeyCode(51, "AC12", ScanCode(0x2B)),  # not in basic
        # KeyCode(51, "BKSL", ScanCode(0x2B)),  # not in basic

        KeyCode(50, "LFSH", ScanCode(0x2A)),
        KeyCode(94, "LSGT", ScanCode(0x56)),  # not in basic
        KeyCode(52, "AB01", ScanCode(0x2C)),
        KeyCode(53, "AB02", ScanCode(0x2D)),
        KeyCode(54, "AB03", ScanCode(0x2E)),
        KeyCode(55, "AB04", ScanCode(0x2F)),
        KeyCode(56, "AB05", ScanCode(0x30)),
        KeyCode(57, "AB06", ScanCode(0x31)),
        KeyCode(58, "AB07", ScanCode(0x32)),
        KeyCode(59, "AB08", ScanCode(0x33)),
        KeyCode(60, "AB09", ScanCode(0x34)),
        KeyCode(61, "AB10", ScanCode(0x35)),
        KeyCode(62, "RTSH", ScanCode(0x36)),

        KeyCode(64, "LALT", ScanCode(0x38)),
        KeyCode(37, "LCTL", ScanCode(0x1D)),
        KeyCode(65, "SPCE", ScanCode(0x39)),
        KeyCode(109, "RCTL", ScanCode(0x1D, 0xE0)),
        KeyCode(113, "RALT", ScanCode(0x38, 0xE0)),
        KeyCode(115, "LWIN", ScanCode(0x5B, 0xE0)),
        KeyCode(116, "RWIN", ScanCode(0x5C, 0xE0)),
        KeyCode(117, "MENU", ScanCode(0x5D, 0xE0)),

        KeyCode(9, "ESC", ScanCode(0x01)),
        KeyCode(67, "FK01", ScanCode(0x3B)),
        KeyCode(68, "FK02", ScanCode(0x3C)),
        KeyCode(69, "FK03", ScanCode(0x3D)),
        KeyCode(70, "FK04", ScanCode(0x3E)),
        KeyCode(71, "FK05", ScanCode(0x3F)),
        KeyCode(72, "FK06", ScanCode(0x40)),
        KeyCode(73, "FK07", ScanCode(0x41)),
        KeyCode(74, "FK08", ScanCode(0x42)),
        KeyCode(75, "FK09", ScanCode(0x43)),
        KeyCode(76, "FK10", ScanCode(0x44)),
        KeyCode(95, "FK11", ScanCode(0x57)),
        KeyCode(96, "FK12", ScanCode(0x58)),

        KeyCode(111, "PRSC", ScanCode(0x54)),  # TODO check
        # KeyCode(92, "SYRQ", ScanCode(0)),  # TODO
        # KeyCode(78, "SCLK", ScanCode(0)),  # TODO
        KeyCode(110, "PAUS", ScanCode(0x1D, 0xE1)),
        # KeyCode(114, "BRK", ScanCode(0)),  # TODO

        KeyCode(106, "INS", ScanCode(0x52, 0xE0)),
        KeyCode(97, "HOME", ScanCode(0x47, 0xE0)),
        KeyCode(99, "PGUP", ScanCode(0x49, 0xE0)),
        KeyCode(107, "DELE", ScanCode(0x53, 0xE0)),
        KeyCode(103, "END", ScanCode(0x4F, 0xE0)),
        KeyCode(105, "PGDN", ScanCode(0x51, 0xE0)),

        KeyCode(98, "UP", ScanCode(0x48, 0xE0)),
        KeyCode(100, "LEFT", ScanCode(0x4B, 0xE0)),
        KeyCode(104, "DOWN", ScanCode(0x50, 0xE0)),
        KeyCode(102, "RIGHT", ScanCode(0x4D, 0xE0)),

        KeyCode(77, "NMLK", ScanCode(0x45)),  # TODO check prefix
        KeyCode(112, "KPDV", ScanCode(0x35, 0xE0)),
        KeyCode(63, "KPMU", ScanCode(0x37)),
        KeyCode(82, "KPSU", ScanCode(0x4A)),

        KeyCode(79, "KP7", ScanCode(0x47)),
        KeyCode(80, "KP8", ScanCode(0x48)),
        KeyCode(81, "KP9", ScanCode(0x49)),
        KeyCode(86, "KPAD", ScanCode(0x4E)),

        KeyCode(83, "KP4", ScanCode(0x4B)),
        KeyCode(84, "KP5", ScanCode(0x4C)),
        KeyCode(85, "KP6", ScanCode(0x4D)),

        KeyCode(87, "KP1", ScanCode(0x4F)),
        KeyCode(88, "KP2", ScanCode(0x50)),
        KeyCode(89, "KP3", ScanCode(0x51)),
        KeyCode(108, "KPEN", ScanCode(0x1C, 0xE0)),

        KeyCode(90, "KP0", ScanCode(0x52)),
        KeyCode(91, "KPDL", ScanCode(0x53)),
        # KeyCode(126, "KPEQ", ScanCode(0))  # TODO

        KeyCode(118, "FK13", ScanCode(0x64)),
        KeyCode(119, "FK14", ScanCode(0x65)),
        KeyCode(120, "FK15", ScanCode(0x66)),
        KeyCode(121, "FK16", ScanCode(0x67)),
        KeyCode(122, "FK17", ScanCode(0x68)),
        # KeyCode(123, "KPDC", ScanCode(0)),  # TODO

        # Japanese keyboards
        # KeyCode(49, "HZTG", ScanCode(0x29)),
        # KeyCode(211, "AB11", ScanCode(0)),  # TODO
        # KeyCode(129, "XFER", ScanCode(0)),  # TODO
        # KeyCode(131, "NFER", ScanCode(0)),  # TODO
        # KeyCode(133, "AE13", ScanCode(0)),  # TODO
        # KeyCode(210, "EISU", ScanCode(0)),  # TODO
        # KeyCode(209, "KANA", ScanCode(0)),  # TODO

        # Korean keyboards
        # KeyCode(121, "HNGL", ScanCode(0x67)),
        # KeyCode(122, "HJCV", ScanCode(0x68)),
    ]

    inet = [
        # media_common
        0x10, 0x19, 0x20, 0x22, 0x24, 0x2E, 0x30,
        # TODO 0x2A, 0x4C, (unknown Windows VSC mappings)

        # nav_common
        0x21, 0x32, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D,

        # acpi_common
        0x5E, 0x5F, 0x63,
        # TODO 0x74, 0x76, 0x16 (unknown Windows VSC mappings)
    ]

    for num in inet:
        vsc = ScanCode(num, 0xE0)
        xfree86.append(KeyCode(num + 128, "I%02X" % (num,), vsc))

    for keycode in xfree86:
        print(f"KEY_{keycode.name} = {keycode!r}", file=f)
    print(file=f)

    print("all = [", file=f)
    for key in xfree86:
        print(f"    KEY_{key.name},", file=f)
    print("]", file=f)
    print(file=f)

    print("keycode_to_xfree86 = {", file=f)
    for keycode in sorted(xfree86, key=lambda k: k.code):
        print(f"  {keycode.code}: KEY_{keycode.name},", file=f)
    print("}", file=f)
    print(file=f)

    print("vsc_to_xfree86 = {", file=f)
    for keycode in sorted(xfree86, key=lambda k: k.vsc.to_string()):
        print(f"  {keycode.vsc}: KEY_{keycode.name},", file=f)
    print("}", file=f)
    print(file=f)



if __name__ == '__main__':
    def _main():
        import sys
        dir, sep, file = __file__.rpartition("_gen_")
        if sep != "_gen_":
            raise RuntimeError("This is the generated file. "
                               "Please run the _gen_ version to regenerate it.")

        if len(sys.argv) != 1:
            # TODO take names from /usr/share/X11/kbd/keycodes/xfree86?
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


