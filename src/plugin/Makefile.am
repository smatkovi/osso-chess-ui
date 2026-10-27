plugindir = @prefix@/lib/osso-chess-ui
plugin_LTLIBRARIES = chess_plugin.la

chess_plugin_la_CFLAGS = $(GTK_CFLAGS) $(GCONF_CFLAGS) $(GLIB_CFLAGS) $(HILDON_CFLAGS) $(OSSO_CFLAGS) \
	-DCHESSLOCALEDIR=\"$(datadir)/locale\"

chess_plugin_la_LDFLAGS = -module -avoid-version

chess_plugin_la_LIBADD = $(GTK_LIBS) $(OSSO_LIBS) $(GCONF_LIBS) $(HILDON_LIBS) \
	$(PANGO_LIBS)

chess_plugin_la_SOURCES = plugin.c
