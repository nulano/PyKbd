
from PIL import Image, ImageDraw, ImageFont

from PyKbd.visualizer import ISO, Keyboard
from PyKbd.data import mac_vk


def draw_key(x, y, w, h, draw: ImageDraw, vk: mac_vk.Vk, font: ImageFont):
    draw.rectangle((x, y, x + w, y + h), outline=(0, 0, 0))
    if vk is None:
        return
    draw.text((x + w / 2, y + h / 2), vk.name[4:], fill=(0, 0, 0), font=font, anchor="mm")


def draw_keyboard(keyboard: Keyboard):
    key_size = 100
    minx, miny, maxx, maxy = keyboard.bounds()
    if (minx, miny, maxx, maxy) == (0, 0, 0, 0):
        return Image.new("RGB", (0, 0))
    # miny -= 0.5  # title
    wd, ht = int((maxx - minx) * key_size + 1), int((maxy - miny) * key_size + 1)
    im = Image.new("RGB", (wd, ht), (255, 255, 255))
    draw = ImageDraw.Draw(im, "RGB")
    font = ImageFont.truetype('SFNS', 12)
    # draw_text(draw, (maxx - minx) * key_size / 2, 0.25 * key_size, font, layout.name + " by " + layout.author)
    for bounds, scancode, special in keyboard:
        x1, y1, x2, y2 = bounds
        draw_key(
            (x1 - minx) * key_size,
            (y1 - miny) * key_size,
            (x2 - x1) * key_size,
            (y2 - y1) * key_size,
            draw,
            mac_vk.vsc_to_vk.get((scancode.prefix << 8) | scancode.code),
            font,
        )
    return im


draw_keyboard(ISO).show()
