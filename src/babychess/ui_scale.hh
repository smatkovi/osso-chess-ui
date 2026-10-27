#ifndef UI_SCALE_INCLUDED
#define UI_SCALE_INCLUDED

/* The N900's layout was drawn for a screen 480 pixels high. On a larger
 * screen (1080 on the F(x)tec Pro1X) the control panel's pictures and
 * positions are scaled by its height over 480, at least 1; CHESS_UI_SCALE
 * in the environment overrides it. The board scales itself to its widget.
 */

double Chess_UI_Scale();

/* The control panel's pictures are drawn at this many times the N900's
 * size (data/make-art.py), and scaled down to the screen's */
#define CHESS_ART_SCALE 3

/* A length of the N900's layout on this screen */
#define UI_LENGTH(v) ((int) ((v) * Chess_UI_Scale() + 0.5))

#endif /* ! UI_SCALE_INCLUDED */
