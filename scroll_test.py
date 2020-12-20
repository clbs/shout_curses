#from __future__ import division  #You don't need this in Python3
import curses
from math import *
from shoutcast_data import ShoutCast
from player import VLCPlayer
from os import getenv as getenv
import dotenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())



screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad( 1 )
curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
highlightText = curses.color_pair( 1 )
normalText = curses.A_NORMAL
screen.border( 0 )
curses.curs_set( 0 )
max_row = 10 #max number of rows
height = 100
width = 100
box = curses.newwin( max_row + 2, 100, 10, 1 )
box.box()

vlc = VLCPlayer()

sc = ShoutCast(getenv('SHOUTCAST_API_KEY'), 'json')
search_items = sc.search("dnb")
search_item_stations = search_items['response']['data']['stationlist']['station']
search_item_titles = list(map(lambda x: x['name'], search_items['response']['data']['stationlist']['station']))
strings = search_item_titles 
row_num = len( strings )

pages = int( ceil( row_num / max_row ) )
position = 1
page = 1
for i in range( 1, max_row + 1 ):
    if row_num == 0:
        box.addstr( 1, 1, "There aren't strings", highlightText )
    else:
        if (i == position):
            box.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
        else:
            box.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], normalText )
        if i == row_num:
            break

screen.refresh()
box.refresh()

x = screen.getch()
while x != 27:
    if x == curses.KEY_DOWN:
        if page == 1:
            if position < i:
                position = position + 1
            else:
                if pages > 1:
                    page = page + 1
                    position = 1 + ( max_row * ( page - 1 ) )
        elif page == pages:
            if position < row_num:
                position = position + 1
        else:
            if position < max_row + ( max_row * ( page - 1 ) ):
                position = position + 1
            else:
                page = page + 1
                position = 1 + ( max_row * ( page - 1 ) )
    if x == curses.KEY_UP:
        if page == 1:
            if position > 1:
                position = position - 1
        else:
            if position > ( 1 + ( max_row * ( page - 1 ) ) ):
                position = position - 1
            else:
                page = page - 1
                position = max_row + ( max_row * ( page - 1 ) )
    if x == curses.KEY_LEFT:
        if page > 1:
            page = page - 1
            position = 1 + ( max_row * ( page - 1 ) )

    if x == curses.KEY_RIGHT:
        if page < pages:
            page = page + 1
            position = ( 1 + ( max_row * ( page - 1 ) ) )
    if x == ord( "\n" ) and row_num != 0:
        screen.erase()
        screen.border( 0 )
        station_id = str(search_item_stations[position - 1]['id'])
        screen.addstr( 23, 3, "YOU HAVE PRESSED '" + strings[ position - 1 ] + "' ON POSITION " + str( position ) )
        screen.addstr( 24, 3, "STATION ID: " + station_id)
        screen.addstr( 25, 3, "STATION URL: " + sc.station_info(station_id)['locations'][0])
        vlc.stream_media(sc.station_info(station_id)['locations'][0])
        
    if x == ord("/"):
        screen.erase()
        screen.border(0)
        screen.addstr(1,1, 'Search for a stream:', curses.A_BOLD)
        #window1, panel1 = create_panel('Results', 30, 50, 5, 11)
        #curses.panel.update_panels()
        screen.refresh()
        screen.move(10,26)
        curses.echo()
        search_string = screen.getstr(1,26, 20)
        curses.noecho()
        search_items = sc.search(search_string.decode('utf-8'))
        search_item_stations = search_items['response']['data']['stationlist']['station']
        search_item_titles = list(map(lambda x: x['name'], search_items['response']['data']['stationlist']['station']))
        box = curses.newwin( max_row + 2, 100, 10, 1 )
        box.box()
        strings = search_item_titles 
        row_num = len( strings )
        pages = int( ceil( row_num / max_row ) )
        position = 1
        page = 1
        for i in range( 1, max_row + 1 ):
            if row_num == 0:
                box.addstr( 1, 1, "There aren't strings", highlightText )
            else:
                if (i == position):
                    box.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
                else:
                    box.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], normalText )
                if i == row_num:
                    break

        screen.refresh()
        box.refresh()
        screen.border( 0 )
        box.border( 0 )

    for i in range( 1 + ( max_row * ( page - 1 ) ), max_row + 1 + ( max_row * ( page - 1 ) ) ):
        if row_num == 0:
            box.addstr( 1, 1, "There aren't strings",  highlightText )
        else:
            if ( i + ( max_row * ( page - 1 ) ) == position + ( max_row * ( page - 1 ) ) ):
                box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
            else:
                box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + strings[ i - 1 ], normalText )
            if i == row_num:
                break



    screen.refresh()
    box.refresh()
    x = screen.getch()

curses.endwin()
exit()
