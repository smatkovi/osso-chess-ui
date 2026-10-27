#include "ui_scale.hh"

#include <stdlib.h>
#include <gdk/gdk.h>

double Chess_UI_Scale()
{
	static double scale = 0;

	if (scale == 0)
	{
		const char *env = getenv("CHESS_UI_SCALE");
		GdkScreen *screen = gdk_screen_get_default();

		if (env && atof(env) > 0)
			scale = atof(env);
		else if (screen)
		{
			int w = gdk_screen_get_width(screen);
			int h = gdk_screen_get_height(screen);
			/* landscape: the shorter side */
			scale = (w < h ? w : h) / 480.0;
		}
		if (scale < 1)
			scale = 1;
	}
	return scale;
}
