# osso-chess-ui: the Nokia N900's Chess for Maemo Leste and FreeBSD

The chess game of Maemo 5 (Fremantle), from Nokia's GPL sources
(`maemo-leste-extras/osso-chess-ui`), ported to today's Maemo Leste and
to Hildon on FreeBSD. It plays against GNU Chess and is started from
`osso-games-startup`, as on the N900.

What changed (see `debian/changelog`):

- GIO instead of GnomeVFS; GNU Chess 6's replies; builds with `$(CXX)`.
- **Own pictures.** The N900's board, pieces and buttons were Nokia's
  (`osso-graphics-game-chess`, not free) and are not used: the pieces are
  Colin M. L. Burnett's (Wikimedia Commons, GPL/BSD/GFDL,
  `data/art/cburnett/`), the control panel is drawn by `data/make-art.py`,
  the board, its frame and the marks on it are drawn by the program.
- **Scales with the screen**: the board fills the screen's height, the
  control panel is scaled by the screen's height over 480 (2.25 on the
  F(x)tec Pro1X); `CHESS_UI_SCALE` overrides it.
- **Tap to move**: a tap on a piece, then a tap on where it goes.

Sounds: `osso-sounds-game-chess` (Leste's archive) where installed.

## Build

Debian/Leste: `dpkg-buildpackage -b -us -uc` (needs Leste's
`osso-games-startup-dev`, `libcomapp-dev`, `libhildonfm2-dev`, ...;
`gnuchess` at run time). FreeBSD: part of
[pro1x-maemo-leste](https://github.com/smatkovi/pro1x-maemo-leste)'s
`freebsd/hildon` build (`--with-gnuchess=/usr/local/bin/gnuchess`).

To redraw the pictures: `python3 data/make-art.py` (rsvg-convert, Pillow).

## Licence

GPL 2 or later (Nokia's code, BabyChess by Sebastian Pipping); the pieces
under the GPL, as allowed by their author's choice of licences.
