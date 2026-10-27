#!/usr/bin/env python3
"""Draws the pieces and the control panel of osso-chess-ui into data/: the
pictures the program loads from its pixmaps directory, which on the N900
were Nokia's and are not part of this source. The board, its frame and
the marks on it are drawn by the program itself (src/babychess), at any
size, in the colours of src/babychess/board_defaults.cc.

The pieces are Colin M. L. Burnett's (art/cburnett/, from Wikimedia
Commons, under the GPL, a BSD licence or the GFDL), at 160 pixels (the
program scales them to its squares). The control panel is drawn at
ART_SCALE times the N900's size; the program scales it to the screen
(src/babychess/ui_scale.hh, CHESS_ART_SCALE).

    python3 data/make-art.py      (needs rsvg-convert and Pillow)
"""
import io
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "art")

PIECE = 160
ART_SCALE = 3
LIGHT, DARK = (240, 217, 181), (181, 136, 99)
FRAME = (46, 52, 58)
PANEL = (58, 65, 72)
WELL = (32, 36, 40)
TEXT = (225, 228, 230)
DIM = (120, 126, 132)
ACCENT = (255, 196, 0)


def font(size):
    for f in ("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/local/share/fonts/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def svg(path, size):
    png = subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), path],
                         check=True, capture_output=True).stdout
    return Image.open(io.BytesIO(png)).convert("RGBA")


def piece(p, colour, size):
    return svg(os.path.join(ART, "cburnett", "Chess_%s%st45.svg" % (p, colour)), size)


def pieces(shadow):
    # row 0 black, row 1 white (chess_color.hh); P N B R Q K (piece_type.hh)
    sq = PIECE
    out = Image.new("RGBA", (6 * sq, 2 * sq), (0, 0, 0, 0))
    for row, colour in enumerate("dl"):
        for col, p in enumerate("pnbrqk"):
            im = piece(p, colour, sq * 15 // 16)
            x, y = col * sq + sq // 32, row * sq + sq // 32
            if shadow:
                sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
                sh.putalpha(im.getchannel("A").point(lambda a: int(a * 0.45)))
                out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(sq // 28)),
                                    (x + sq // 28, y + sq // 28))
            out.alpha_composite(im, (x, y))
    return out


def centred(d, box, text, fnt, fill):
    l, t, r, b = d.textbbox((0, 0), text, font=fnt)
    x = box[0] + (box[2] - box[0] - (r - l)) / 2 - l
    y = box[1] + (box[3] - box[1] - (b - t)) / 2 - t
    d.text((x, y), text, font=fnt, fill=fill)


def K(*v):
    """Lengths of the N900's layout at ART_SCALE"""
    return [x * ART_SCALE for x in v] if len(v) > 1 else v[0] * ART_SCALE


def rounded(d, box, fill, outline=None, radius=10, width=2):
    d.rounded_rectangle(K(*box), radius=K(radius), fill=fill, outline=outline,
                        width=K(width))


def control():
    """The panel right of the board, 310x480: the moves list from (38, 15),
    the black and white players at (31, 255) and (31, 312), undo and redo
    at (68, 390) and (174, 390), the back button at (180, 0)
    (src/ui/interface.hh)."""
    im = Image.new("RGB", K(310, 480), FRAME)
    d = ImageDraw.Draw(im)
    rounded(d, (20, 70, 290, 238), WELL, PANEL)
    rounded(d, (20, 248, 300, 374), PANEL)
    rounded(d, (20, 382, 300, 474), PANEL)
    return im


def buttons(state):
    """Undo and redo side by side, 2x 76x76."""
    im = Image.new("RGB", K(152, 76), PANEL)
    d = ImageDraw.Draw(im)
    face = {"normal": (82, 92, 102), "pressed": ACCENT, "dimmed": (66, 72, 78)}[state]
    arrow = {"normal": TEXT, "pressed": WELL, "dimmed": DIM}[state]
    for i, sign in enumerate((-1, 1)):
        x0 = i * 76
        rounded(d, (x0 + 6, 6, x0 + 69, 69), face, radius=12)
        cx, cy = x0 + 38, 38
        d.polygon([K(cx + 12 * sign, cy), K(cx - 8 * sign, cy - 16), K(cx - 8 * sign, cy + 16)],
                  fill=arrow)
    return im


def status(active):
    """The two players, white left and black right, 2x 262x54; the
    program writes the name right of the king (src/ui/chess_status.cc)."""
    im = Image.new("RGBA", K(524, 54), PANEL + (255,))
    d = ImageDraw.Draw(im)
    for i, colour in enumerate("ld"):
        x0 = i * 262
        rounded(d, (x0 + 2, 2, x0 + 259, 51), (250, 250, 248) if active else (150, 156, 162),
                outline=ACCENT if active else None, radius=8, width=3)
        k = piece("k", colour, K(42))
        if not active:
            k.putalpha(k.getchannel("A").point(lambda a: a // 2))
        im.alpha_composite(k, tuple(K(x0 + 8, 6)))
    return im.convert("RGB")


def startup():
    """osso-games-startup's picture of the game, 668x179 (shown as it is)."""
    im = Image.new("RGBA", (668, 179), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 667, 178), radius=16, fill=FRAME + (255,))
    for i in range(15):
        x = 24 + i * 20
        d.rectangle([x, 140, x + 19, 159], fill=LIGHT if i % 2 == 0 else DARK)
    for i, (p, c) in enumerate((("r", "d"), ("n", "l"), ("k", "l"), ("q", "d"))):
        size = 96 if p in "kq" else 80
        im.alpha_composite(piece(p, c, size), (24 + i * 72, 146 - size))
    centred(d, (330, 20, 650, 160), "Chess", font(64), TEXT)
    return im


def main():
    os.chdir(HERE)
    pieces(False).save("pieces.png")
    pieces(True).save("pieces_with_shadow.png")
    control().save("Background_control.jpg", quality=92)
    buttons("normal").save("Undo_Redo.jpg", quality=92)
    buttons("pressed").save("Undo_Redo_pressed.jpg", quality=92)
    buttons("dimmed").save("Undo_Redo_dimmed.jpg", quality=92)
    status(True).save("Black_White_active.jpg", quality=92)
    status(False).save("Black_White_passive.jpg", quality=92)
    startup().save("osso-games-startup-chess.png")


if __name__ == "__main__":
    sys.exit(main())
