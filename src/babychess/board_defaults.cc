#include "board_defaults.hh"
#include "rgb.hh"

bool Read_Defaults(Stream &stream, 
		 Board_Settings &board)
{
	(void)stream;

	//board.flags = bs_frame | bs_smooth | bs_tutor;
	board.flags = bs_frame | bs_tutor | bs_smooth;
	/* the board's colours (data/make-art.py draws the rest to match) */
	board.colors[c_light]=RGB(240,217,181);
	board.colors[c_dark]=RGB(181,136,99);
	board.colors[c_last_move]=RGB(252,254,115);
	board.colors[c_frame]=RGB(46,52,58);
	board.colors[c_highlight]=RGB(255,196,0);
	board.colors[c_text]=RGB(225,228,230);
	int i;
	for (i=c_text+1; i<c_count; i++)
		board.colors[i]=RGB(0,0,0);

	return true;
}
