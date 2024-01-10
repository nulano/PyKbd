# ----- DO NOT EDIT THIS GENERATED FILE -----

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



KEY_TLDE = KeyCode(code=49, name='TLDE', vsc=ScanCode(code=41, prefix=0))
KEY_AE01 = KeyCode(code=10, name='AE01', vsc=ScanCode(code=2, prefix=0))
KEY_AE02 = KeyCode(code=11, name='AE02', vsc=ScanCode(code=3, prefix=0))
KEY_AE03 = KeyCode(code=12, name='AE03', vsc=ScanCode(code=4, prefix=0))
KEY_AE04 = KeyCode(code=13, name='AE04', vsc=ScanCode(code=5, prefix=0))
KEY_AE05 = KeyCode(code=14, name='AE05', vsc=ScanCode(code=6, prefix=0))
KEY_AE06 = KeyCode(code=15, name='AE06', vsc=ScanCode(code=7, prefix=0))
KEY_AE07 = KeyCode(code=16, name='AE07', vsc=ScanCode(code=8, prefix=0))
KEY_AE08 = KeyCode(code=17, name='AE08', vsc=ScanCode(code=9, prefix=0))
KEY_AE09 = KeyCode(code=18, name='AE09', vsc=ScanCode(code=10, prefix=0))
KEY_AE10 = KeyCode(code=19, name='AE10', vsc=ScanCode(code=11, prefix=0))
KEY_AE11 = KeyCode(code=20, name='AE11', vsc=ScanCode(code=12, prefix=0))
KEY_AE12 = KeyCode(code=21, name='AE12', vsc=ScanCode(code=13, prefix=0))
KEY_BKSP = KeyCode(code=22, name='BKSP', vsc=ScanCode(code=14, prefix=0))
KEY_TAB = KeyCode(code=23, name='TAB', vsc=ScanCode(code=15, prefix=0))
KEY_AD01 = KeyCode(code=24, name='AD01', vsc=ScanCode(code=16, prefix=0))
KEY_AD02 = KeyCode(code=25, name='AD02', vsc=ScanCode(code=17, prefix=0))
KEY_AD03 = KeyCode(code=26, name='AD03', vsc=ScanCode(code=18, prefix=0))
KEY_AD04 = KeyCode(code=27, name='AD04', vsc=ScanCode(code=19, prefix=0))
KEY_AD05 = KeyCode(code=28, name='AD05', vsc=ScanCode(code=20, prefix=0))
KEY_AD06 = KeyCode(code=29, name='AD06', vsc=ScanCode(code=21, prefix=0))
KEY_AD07 = KeyCode(code=30, name='AD07', vsc=ScanCode(code=22, prefix=0))
KEY_AD08 = KeyCode(code=31, name='AD08', vsc=ScanCode(code=23, prefix=0))
KEY_AD09 = KeyCode(code=32, name='AD09', vsc=ScanCode(code=24, prefix=0))
KEY_AD10 = KeyCode(code=33, name='AD10', vsc=ScanCode(code=25, prefix=0))
KEY_AD11 = KeyCode(code=34, name='AD11', vsc=ScanCode(code=26, prefix=0))
KEY_AD12 = KeyCode(code=35, name='AD12', vsc=ScanCode(code=27, prefix=0))
KEY_RTRN = KeyCode(code=36, name='RTRN', vsc=ScanCode(code=28, prefix=0))
KEY_CAPS = KeyCode(code=66, name='CAPS', vsc=ScanCode(code=58, prefix=0))
KEY_AC01 = KeyCode(code=38, name='AC01', vsc=ScanCode(code=30, prefix=0))
KEY_AC02 = KeyCode(code=39, name='AC02', vsc=ScanCode(code=31, prefix=0))
KEY_AC03 = KeyCode(code=40, name='AC03', vsc=ScanCode(code=32, prefix=0))
KEY_AC04 = KeyCode(code=41, name='AC04', vsc=ScanCode(code=33, prefix=0))
KEY_AC05 = KeyCode(code=42, name='AC05', vsc=ScanCode(code=34, prefix=0))
KEY_AC06 = KeyCode(code=43, name='AC06', vsc=ScanCode(code=35, prefix=0))
KEY_AC07 = KeyCode(code=44, name='AC07', vsc=ScanCode(code=36, prefix=0))
KEY_AC08 = KeyCode(code=45, name='AC08', vsc=ScanCode(code=37, prefix=0))
KEY_AC09 = KeyCode(code=46, name='AC09', vsc=ScanCode(code=38, prefix=0))
KEY_AC10 = KeyCode(code=47, name='AC10', vsc=ScanCode(code=39, prefix=0))
KEY_AC11 = KeyCode(code=48, name='AC11', vsc=ScanCode(code=40, prefix=0))
KEY_AC12 = KeyCode(code=51, name='AC12', vsc=ScanCode(code=43, prefix=0))
KEY_LFSH = KeyCode(code=50, name='LFSH', vsc=ScanCode(code=42, prefix=0))
KEY_LSGT = KeyCode(code=94, name='LSGT', vsc=ScanCode(code=86, prefix=0))
KEY_AB01 = KeyCode(code=52, name='AB01', vsc=ScanCode(code=44, prefix=0))
KEY_AB02 = KeyCode(code=53, name='AB02', vsc=ScanCode(code=45, prefix=0))
KEY_AB03 = KeyCode(code=54, name='AB03', vsc=ScanCode(code=46, prefix=0))
KEY_AB04 = KeyCode(code=55, name='AB04', vsc=ScanCode(code=47, prefix=0))
KEY_AB05 = KeyCode(code=56, name='AB05', vsc=ScanCode(code=48, prefix=0))
KEY_AB06 = KeyCode(code=57, name='AB06', vsc=ScanCode(code=49, prefix=0))
KEY_AB07 = KeyCode(code=58, name='AB07', vsc=ScanCode(code=50, prefix=0))
KEY_AB08 = KeyCode(code=59, name='AB08', vsc=ScanCode(code=51, prefix=0))
KEY_AB09 = KeyCode(code=60, name='AB09', vsc=ScanCode(code=52, prefix=0))
KEY_AB10 = KeyCode(code=61, name='AB10', vsc=ScanCode(code=53, prefix=0))
KEY_RTSH = KeyCode(code=62, name='RTSH', vsc=ScanCode(code=54, prefix=0))
KEY_LALT = KeyCode(code=64, name='LALT', vsc=ScanCode(code=56, prefix=0))
KEY_LCTL = KeyCode(code=37, name='LCTL', vsc=ScanCode(code=29, prefix=0))
KEY_SPCE = KeyCode(code=65, name='SPCE', vsc=ScanCode(code=57, prefix=0))
KEY_RCTL = KeyCode(code=109, name='RCTL', vsc=ScanCode(code=29, prefix=224))
KEY_RALT = KeyCode(code=113, name='RALT', vsc=ScanCode(code=56, prefix=224))
KEY_LWIN = KeyCode(code=115, name='LWIN', vsc=ScanCode(code=91, prefix=224))
KEY_RWIN = KeyCode(code=116, name='RWIN', vsc=ScanCode(code=92, prefix=224))
KEY_MENU = KeyCode(code=117, name='MENU', vsc=ScanCode(code=93, prefix=224))
KEY_ESC = KeyCode(code=9, name='ESC', vsc=ScanCode(code=1, prefix=0))
KEY_FK01 = KeyCode(code=67, name='FK01', vsc=ScanCode(code=59, prefix=0))
KEY_FK02 = KeyCode(code=68, name='FK02', vsc=ScanCode(code=60, prefix=0))
KEY_FK03 = KeyCode(code=69, name='FK03', vsc=ScanCode(code=61, prefix=0))
KEY_FK04 = KeyCode(code=70, name='FK04', vsc=ScanCode(code=62, prefix=0))
KEY_FK05 = KeyCode(code=71, name='FK05', vsc=ScanCode(code=63, prefix=0))
KEY_FK06 = KeyCode(code=72, name='FK06', vsc=ScanCode(code=64, prefix=0))
KEY_FK07 = KeyCode(code=73, name='FK07', vsc=ScanCode(code=65, prefix=0))
KEY_FK08 = KeyCode(code=74, name='FK08', vsc=ScanCode(code=66, prefix=0))
KEY_FK09 = KeyCode(code=75, name='FK09', vsc=ScanCode(code=67, prefix=0))
KEY_FK10 = KeyCode(code=76, name='FK10', vsc=ScanCode(code=68, prefix=0))
KEY_FK11 = KeyCode(code=95, name='FK11', vsc=ScanCode(code=87, prefix=0))
KEY_FK12 = KeyCode(code=96, name='FK12', vsc=ScanCode(code=88, prefix=0))
KEY_PRSC = KeyCode(code=111, name='PRSC', vsc=ScanCode(code=84, prefix=0))
KEY_PAUS = KeyCode(code=110, name='PAUS', vsc=ScanCode(code=29, prefix=225))
KEY_INS = KeyCode(code=106, name='INS', vsc=ScanCode(code=82, prefix=224))
KEY_HOME = KeyCode(code=97, name='HOME', vsc=ScanCode(code=71, prefix=224))
KEY_PGUP = KeyCode(code=99, name='PGUP', vsc=ScanCode(code=73, prefix=224))
KEY_DELE = KeyCode(code=107, name='DELE', vsc=ScanCode(code=83, prefix=224))
KEY_END = KeyCode(code=103, name='END', vsc=ScanCode(code=79, prefix=224))
KEY_PGDN = KeyCode(code=105, name='PGDN', vsc=ScanCode(code=81, prefix=224))
KEY_UP = KeyCode(code=98, name='UP', vsc=ScanCode(code=72, prefix=224))
KEY_LEFT = KeyCode(code=100, name='LEFT', vsc=ScanCode(code=75, prefix=224))
KEY_DOWN = KeyCode(code=104, name='DOWN', vsc=ScanCode(code=80, prefix=224))
KEY_RIGHT = KeyCode(code=102, name='RIGHT', vsc=ScanCode(code=77, prefix=224))
KEY_NMLK = KeyCode(code=77, name='NMLK', vsc=ScanCode(code=69, prefix=0))
KEY_KPDV = KeyCode(code=112, name='KPDV', vsc=ScanCode(code=53, prefix=224))
KEY_KPMU = KeyCode(code=63, name='KPMU', vsc=ScanCode(code=55, prefix=0))
KEY_KPSU = KeyCode(code=82, name='KPSU', vsc=ScanCode(code=74, prefix=0))
KEY_KP7 = KeyCode(code=79, name='KP7', vsc=ScanCode(code=71, prefix=0))
KEY_KP8 = KeyCode(code=80, name='KP8', vsc=ScanCode(code=72, prefix=0))
KEY_KP9 = KeyCode(code=81, name='KP9', vsc=ScanCode(code=73, prefix=0))
KEY_KPAD = KeyCode(code=86, name='KPAD', vsc=ScanCode(code=78, prefix=0))
KEY_KP4 = KeyCode(code=83, name='KP4', vsc=ScanCode(code=75, prefix=0))
KEY_KP5 = KeyCode(code=84, name='KP5', vsc=ScanCode(code=76, prefix=0))
KEY_KP6 = KeyCode(code=85, name='KP6', vsc=ScanCode(code=77, prefix=0))
KEY_KP1 = KeyCode(code=87, name='KP1', vsc=ScanCode(code=79, prefix=0))
KEY_KP2 = KeyCode(code=88, name='KP2', vsc=ScanCode(code=80, prefix=0))
KEY_KP3 = KeyCode(code=89, name='KP3', vsc=ScanCode(code=81, prefix=0))
KEY_KPEN = KeyCode(code=108, name='KPEN', vsc=ScanCode(code=28, prefix=224))
KEY_KP0 = KeyCode(code=90, name='KP0', vsc=ScanCode(code=82, prefix=0))
KEY_KPDL = KeyCode(code=91, name='KPDL', vsc=ScanCode(code=83, prefix=0))
KEY_FK13 = KeyCode(code=118, name='FK13', vsc=ScanCode(code=100, prefix=0))
KEY_FK14 = KeyCode(code=119, name='FK14', vsc=ScanCode(code=101, prefix=0))
KEY_FK15 = KeyCode(code=120, name='FK15', vsc=ScanCode(code=102, prefix=0))
KEY_FK16 = KeyCode(code=121, name='FK16', vsc=ScanCode(code=103, prefix=0))
KEY_FK17 = KeyCode(code=122, name='FK17', vsc=ScanCode(code=104, prefix=0))
KEY_I10 = KeyCode(code=144, name='I10', vsc=ScanCode(code=16, prefix=224))
KEY_I19 = KeyCode(code=153, name='I19', vsc=ScanCode(code=25, prefix=224))
KEY_I20 = KeyCode(code=160, name='I20', vsc=ScanCode(code=32, prefix=224))
KEY_I22 = KeyCode(code=162, name='I22', vsc=ScanCode(code=34, prefix=224))
KEY_I24 = KeyCode(code=164, name='I24', vsc=ScanCode(code=36, prefix=224))
KEY_I2E = KeyCode(code=174, name='I2E', vsc=ScanCode(code=46, prefix=224))
KEY_I30 = KeyCode(code=176, name='I30', vsc=ScanCode(code=48, prefix=224))
KEY_I21 = KeyCode(code=161, name='I21', vsc=ScanCode(code=33, prefix=224))
KEY_I32 = KeyCode(code=178, name='I32', vsc=ScanCode(code=50, prefix=224))
KEY_I65 = KeyCode(code=229, name='I65', vsc=ScanCode(code=101, prefix=224))
KEY_I66 = KeyCode(code=230, name='I66', vsc=ScanCode(code=102, prefix=224))
KEY_I67 = KeyCode(code=231, name='I67', vsc=ScanCode(code=103, prefix=224))
KEY_I68 = KeyCode(code=232, name='I68', vsc=ScanCode(code=104, prefix=224))
KEY_I69 = KeyCode(code=233, name='I69', vsc=ScanCode(code=105, prefix=224))
KEY_I6A = KeyCode(code=234, name='I6A', vsc=ScanCode(code=106, prefix=224))
KEY_I6B = KeyCode(code=235, name='I6B', vsc=ScanCode(code=107, prefix=224))
KEY_I6C = KeyCode(code=236, name='I6C', vsc=ScanCode(code=108, prefix=224))
KEY_I6D = KeyCode(code=237, name='I6D', vsc=ScanCode(code=109, prefix=224))
KEY_I5E = KeyCode(code=222, name='I5E', vsc=ScanCode(code=94, prefix=224))
KEY_I5F = KeyCode(code=223, name='I5F', vsc=ScanCode(code=95, prefix=224))
KEY_I63 = KeyCode(code=227, name='I63', vsc=ScanCode(code=99, prefix=224))

all = [
    KEY_TLDE,
    KEY_AE01,
    KEY_AE02,
    KEY_AE03,
    KEY_AE04,
    KEY_AE05,
    KEY_AE06,
    KEY_AE07,
    KEY_AE08,
    KEY_AE09,
    KEY_AE10,
    KEY_AE11,
    KEY_AE12,
    KEY_BKSP,
    KEY_TAB,
    KEY_AD01,
    KEY_AD02,
    KEY_AD03,
    KEY_AD04,
    KEY_AD05,
    KEY_AD06,
    KEY_AD07,
    KEY_AD08,
    KEY_AD09,
    KEY_AD10,
    KEY_AD11,
    KEY_AD12,
    KEY_RTRN,
    KEY_CAPS,
    KEY_AC01,
    KEY_AC02,
    KEY_AC03,
    KEY_AC04,
    KEY_AC05,
    KEY_AC06,
    KEY_AC07,
    KEY_AC08,
    KEY_AC09,
    KEY_AC10,
    KEY_AC11,
    KEY_AC12,
    KEY_LFSH,
    KEY_LSGT,
    KEY_AB01,
    KEY_AB02,
    KEY_AB03,
    KEY_AB04,
    KEY_AB05,
    KEY_AB06,
    KEY_AB07,
    KEY_AB08,
    KEY_AB09,
    KEY_AB10,
    KEY_RTSH,
    KEY_LALT,
    KEY_LCTL,
    KEY_SPCE,
    KEY_RCTL,
    KEY_RALT,
    KEY_LWIN,
    KEY_RWIN,
    KEY_MENU,
    KEY_ESC,
    KEY_FK01,
    KEY_FK02,
    KEY_FK03,
    KEY_FK04,
    KEY_FK05,
    KEY_FK06,
    KEY_FK07,
    KEY_FK08,
    KEY_FK09,
    KEY_FK10,
    KEY_FK11,
    KEY_FK12,
    KEY_PRSC,
    KEY_PAUS,
    KEY_INS,
    KEY_HOME,
    KEY_PGUP,
    KEY_DELE,
    KEY_END,
    KEY_PGDN,
    KEY_UP,
    KEY_LEFT,
    KEY_DOWN,
    KEY_RIGHT,
    KEY_NMLK,
    KEY_KPDV,
    KEY_KPMU,
    KEY_KPSU,
    KEY_KP7,
    KEY_KP8,
    KEY_KP9,
    KEY_KPAD,
    KEY_KP4,
    KEY_KP5,
    KEY_KP6,
    KEY_KP1,
    KEY_KP2,
    KEY_KP3,
    KEY_KPEN,
    KEY_KP0,
    KEY_KPDL,
    KEY_FK13,
    KEY_FK14,
    KEY_FK15,
    KEY_FK16,
    KEY_FK17,
    KEY_I10,
    KEY_I19,
    KEY_I20,
    KEY_I22,
    KEY_I24,
    KEY_I2E,
    KEY_I30,
    KEY_I21,
    KEY_I32,
    KEY_I65,
    KEY_I66,
    KEY_I67,
    KEY_I68,
    KEY_I69,
    KEY_I6A,
    KEY_I6B,
    KEY_I6C,
    KEY_I6D,
    KEY_I5E,
    KEY_I5F,
    KEY_I63,
]

keycode_to_xfree86 = {
  9: KEY_ESC,
  10: KEY_AE01,
  11: KEY_AE02,
  12: KEY_AE03,
  13: KEY_AE04,
  14: KEY_AE05,
  15: KEY_AE06,
  16: KEY_AE07,
  17: KEY_AE08,
  18: KEY_AE09,
  19: KEY_AE10,
  20: KEY_AE11,
  21: KEY_AE12,
  22: KEY_BKSP,
  23: KEY_TAB,
  24: KEY_AD01,
  25: KEY_AD02,
  26: KEY_AD03,
  27: KEY_AD04,
  28: KEY_AD05,
  29: KEY_AD06,
  30: KEY_AD07,
  31: KEY_AD08,
  32: KEY_AD09,
  33: KEY_AD10,
  34: KEY_AD11,
  35: KEY_AD12,
  36: KEY_RTRN,
  37: KEY_LCTL,
  38: KEY_AC01,
  39: KEY_AC02,
  40: KEY_AC03,
  41: KEY_AC04,
  42: KEY_AC05,
  43: KEY_AC06,
  44: KEY_AC07,
  45: KEY_AC08,
  46: KEY_AC09,
  47: KEY_AC10,
  48: KEY_AC11,
  49: KEY_TLDE,
  50: KEY_LFSH,
  51: KEY_AC12,
  52: KEY_AB01,
  53: KEY_AB02,
  54: KEY_AB03,
  55: KEY_AB04,
  56: KEY_AB05,
  57: KEY_AB06,
  58: KEY_AB07,
  59: KEY_AB08,
  60: KEY_AB09,
  61: KEY_AB10,
  62: KEY_RTSH,
  63: KEY_KPMU,
  64: KEY_LALT,
  65: KEY_SPCE,
  66: KEY_CAPS,
  67: KEY_FK01,
  68: KEY_FK02,
  69: KEY_FK03,
  70: KEY_FK04,
  71: KEY_FK05,
  72: KEY_FK06,
  73: KEY_FK07,
  74: KEY_FK08,
  75: KEY_FK09,
  76: KEY_FK10,
  77: KEY_NMLK,
  79: KEY_KP7,
  80: KEY_KP8,
  81: KEY_KP9,
  82: KEY_KPSU,
  83: KEY_KP4,
  84: KEY_KP5,
  85: KEY_KP6,
  86: KEY_KPAD,
  87: KEY_KP1,
  88: KEY_KP2,
  89: KEY_KP3,
  90: KEY_KP0,
  91: KEY_KPDL,
  94: KEY_LSGT,
  95: KEY_FK11,
  96: KEY_FK12,
  97: KEY_HOME,
  98: KEY_UP,
  99: KEY_PGUP,
  100: KEY_LEFT,
  102: KEY_RIGHT,
  103: KEY_END,
  104: KEY_DOWN,
  105: KEY_PGDN,
  106: KEY_INS,
  107: KEY_DELE,
  108: KEY_KPEN,
  109: KEY_RCTL,
  110: KEY_PAUS,
  111: KEY_PRSC,
  112: KEY_KPDV,
  113: KEY_RALT,
  115: KEY_LWIN,
  116: KEY_RWIN,
  117: KEY_MENU,
  118: KEY_FK13,
  119: KEY_FK14,
  120: KEY_FK15,
  121: KEY_FK16,
  122: KEY_FK17,
  144: KEY_I10,
  153: KEY_I19,
  160: KEY_I20,
  161: KEY_I21,
  162: KEY_I22,
  164: KEY_I24,
  174: KEY_I2E,
  176: KEY_I30,
  178: KEY_I32,
  222: KEY_I5E,
  223: KEY_I5F,
  227: KEY_I63,
  229: KEY_I65,
  230: KEY_I66,
  231: KEY_I67,
  232: KEY_I68,
  233: KEY_I69,
  234: KEY_I6A,
  235: KEY_I6B,
  236: KEY_I6C,
  237: KEY_I6D,
}

vsc_to_xfree86 = {
  ScanCode(code=1, prefix=0): KEY_ESC,
  ScanCode(code=2, prefix=0): KEY_AE01,
  ScanCode(code=3, prefix=0): KEY_AE02,
  ScanCode(code=4, prefix=0): KEY_AE03,
  ScanCode(code=5, prefix=0): KEY_AE04,
  ScanCode(code=6, prefix=0): KEY_AE05,
  ScanCode(code=7, prefix=0): KEY_AE06,
  ScanCode(code=8, prefix=0): KEY_AE07,
  ScanCode(code=9, prefix=0): KEY_AE08,
  ScanCode(code=10, prefix=0): KEY_AE09,
  ScanCode(code=11, prefix=0): KEY_AE10,
  ScanCode(code=12, prefix=0): KEY_AE11,
  ScanCode(code=13, prefix=0): KEY_AE12,
  ScanCode(code=14, prefix=0): KEY_BKSP,
  ScanCode(code=15, prefix=0): KEY_TAB,
  ScanCode(code=16, prefix=0): KEY_AD01,
  ScanCode(code=17, prefix=0): KEY_AD02,
  ScanCode(code=18, prefix=0): KEY_AD03,
  ScanCode(code=19, prefix=0): KEY_AD04,
  ScanCode(code=20, prefix=0): KEY_AD05,
  ScanCode(code=21, prefix=0): KEY_AD06,
  ScanCode(code=22, prefix=0): KEY_AD07,
  ScanCode(code=23, prefix=0): KEY_AD08,
  ScanCode(code=24, prefix=0): KEY_AD09,
  ScanCode(code=25, prefix=0): KEY_AD10,
  ScanCode(code=26, prefix=0): KEY_AD11,
  ScanCode(code=27, prefix=0): KEY_AD12,
  ScanCode(code=28, prefix=0): KEY_RTRN,
  ScanCode(code=29, prefix=0): KEY_LCTL,
  ScanCode(code=30, prefix=0): KEY_AC01,
  ScanCode(code=31, prefix=0): KEY_AC02,
  ScanCode(code=32, prefix=0): KEY_AC03,
  ScanCode(code=33, prefix=0): KEY_AC04,
  ScanCode(code=34, prefix=0): KEY_AC05,
  ScanCode(code=35, prefix=0): KEY_AC06,
  ScanCode(code=36, prefix=0): KEY_AC07,
  ScanCode(code=37, prefix=0): KEY_AC08,
  ScanCode(code=38, prefix=0): KEY_AC09,
  ScanCode(code=39, prefix=0): KEY_AC10,
  ScanCode(code=40, prefix=0): KEY_AC11,
  ScanCode(code=41, prefix=0): KEY_TLDE,
  ScanCode(code=42, prefix=0): KEY_LFSH,
  ScanCode(code=43, prefix=0): KEY_AC12,
  ScanCode(code=44, prefix=0): KEY_AB01,
  ScanCode(code=45, prefix=0): KEY_AB02,
  ScanCode(code=46, prefix=0): KEY_AB03,
  ScanCode(code=47, prefix=0): KEY_AB04,
  ScanCode(code=48, prefix=0): KEY_AB05,
  ScanCode(code=49, prefix=0): KEY_AB06,
  ScanCode(code=50, prefix=0): KEY_AB07,
  ScanCode(code=51, prefix=0): KEY_AB08,
  ScanCode(code=52, prefix=0): KEY_AB09,
  ScanCode(code=53, prefix=0): KEY_AB10,
  ScanCode(code=54, prefix=0): KEY_RTSH,
  ScanCode(code=55, prefix=0): KEY_KPMU,
  ScanCode(code=56, prefix=0): KEY_LALT,
  ScanCode(code=57, prefix=0): KEY_SPCE,
  ScanCode(code=58, prefix=0): KEY_CAPS,
  ScanCode(code=59, prefix=0): KEY_FK01,
  ScanCode(code=60, prefix=0): KEY_FK02,
  ScanCode(code=61, prefix=0): KEY_FK03,
  ScanCode(code=62, prefix=0): KEY_FK04,
  ScanCode(code=63, prefix=0): KEY_FK05,
  ScanCode(code=64, prefix=0): KEY_FK06,
  ScanCode(code=65, prefix=0): KEY_FK07,
  ScanCode(code=66, prefix=0): KEY_FK08,
  ScanCode(code=67, prefix=0): KEY_FK09,
  ScanCode(code=68, prefix=0): KEY_FK10,
  ScanCode(code=69, prefix=0): KEY_NMLK,
  ScanCode(code=71, prefix=0): KEY_KP7,
  ScanCode(code=72, prefix=0): KEY_KP8,
  ScanCode(code=73, prefix=0): KEY_KP9,
  ScanCode(code=74, prefix=0): KEY_KPSU,
  ScanCode(code=75, prefix=0): KEY_KP4,
  ScanCode(code=76, prefix=0): KEY_KP5,
  ScanCode(code=77, prefix=0): KEY_KP6,
  ScanCode(code=78, prefix=0): KEY_KPAD,
  ScanCode(code=79, prefix=0): KEY_KP1,
  ScanCode(code=80, prefix=0): KEY_KP2,
  ScanCode(code=81, prefix=0): KEY_KP3,
  ScanCode(code=82, prefix=0): KEY_KP0,
  ScanCode(code=83, prefix=0): KEY_KPDL,
  ScanCode(code=84, prefix=0): KEY_PRSC,
  ScanCode(code=86, prefix=0): KEY_LSGT,
  ScanCode(code=87, prefix=0): KEY_FK11,
  ScanCode(code=88, prefix=0): KEY_FK12,
  ScanCode(code=100, prefix=0): KEY_FK13,
  ScanCode(code=101, prefix=0): KEY_FK14,
  ScanCode(code=102, prefix=0): KEY_FK15,
  ScanCode(code=103, prefix=0): KEY_FK16,
  ScanCode(code=104, prefix=0): KEY_FK17,
  ScanCode(code=16, prefix=224): KEY_I10,
  ScanCode(code=25, prefix=224): KEY_I19,
  ScanCode(code=28, prefix=224): KEY_KPEN,
  ScanCode(code=29, prefix=224): KEY_RCTL,
  ScanCode(code=32, prefix=224): KEY_I20,
  ScanCode(code=33, prefix=224): KEY_I21,
  ScanCode(code=34, prefix=224): KEY_I22,
  ScanCode(code=36, prefix=224): KEY_I24,
  ScanCode(code=46, prefix=224): KEY_I2E,
  ScanCode(code=48, prefix=224): KEY_I30,
  ScanCode(code=50, prefix=224): KEY_I32,
  ScanCode(code=53, prefix=224): KEY_KPDV,
  ScanCode(code=56, prefix=224): KEY_RALT,
  ScanCode(code=71, prefix=224): KEY_HOME,
  ScanCode(code=72, prefix=224): KEY_UP,
  ScanCode(code=73, prefix=224): KEY_PGUP,
  ScanCode(code=75, prefix=224): KEY_LEFT,
  ScanCode(code=77, prefix=224): KEY_RIGHT,
  ScanCode(code=79, prefix=224): KEY_END,
  ScanCode(code=80, prefix=224): KEY_DOWN,
  ScanCode(code=81, prefix=224): KEY_PGDN,
  ScanCode(code=82, prefix=224): KEY_INS,
  ScanCode(code=83, prefix=224): KEY_DELE,
  ScanCode(code=91, prefix=224): KEY_LWIN,
  ScanCode(code=92, prefix=224): KEY_RWIN,
  ScanCode(code=93, prefix=224): KEY_MENU,
  ScanCode(code=94, prefix=224): KEY_I5E,
  ScanCode(code=95, prefix=224): KEY_I5F,
  ScanCode(code=99, prefix=224): KEY_I63,
  ScanCode(code=101, prefix=224): KEY_I65,
  ScanCode(code=102, prefix=224): KEY_I66,
  ScanCode(code=103, prefix=224): KEY_I67,
  ScanCode(code=104, prefix=224): KEY_I68,
  ScanCode(code=105, prefix=224): KEY_I69,
  ScanCode(code=106, prefix=224): KEY_I6A,
  ScanCode(code=107, prefix=224): KEY_I6B,
  ScanCode(code=108, prefix=224): KEY_I6C,
  ScanCode(code=109, prefix=224): KEY_I6D,
  ScanCode(code=29, prefix=225): KEY_PAUS,
}

