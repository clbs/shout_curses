#!/usr/bin/env python

import curses
from math import ceil
from shoutcast_data import ShoutCast
from player import VLCPlayer
from user_data import UserData
from os import getenv as getenv
from os import path as path
import dotenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

vlc = VLCPlayer()

user_data = UserData(path.abspath(__file__).replace('main.py', '') + getenv('USER_DATA_CONFIG'))
vlc.set_volume(int(user_data.get_volume()))

screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad(1)
curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
highlightText = curses.color_pair(1)
normalText = curses.A_NORMAL
screen.border(0)
curses.curs_set(0)
max_row = 20 #max number of rows
height = 100
width = 100
height, width = screen.getmaxyx()
box_height = max_row
if height < max_row + 2:
        box_height = height - 2
box = curses.newwin(box_height, width - 2, 1, 1)
message_box = curses.newwin(3, width - 2, max_row + 3, 1)
search_string = ""
message_box_message = "Welcome to Shout Curses"
message_box.box()
box.box()

station_title = ""
station_id = ""
station_url = ""
station_volume = vlc.get_volume()
station_playing = ""
station_mute = ""


sc = ShoutCast(getenv('SHOUTCAST_API_KEY'), 'json')
# this should be removed eventually
stations = user_data.get_stations()
search_items = {}
search_item_stations = stations
favorites = user_data.get_saved_station_ids()
search_item_titles = list(map(lambda x: str("❤ " + x['name'] if int(x['id']) in favorites else x['name']), stations))
strings = search_item_titles
row_num = len(strings)

pages = int(ceil(row_num / max_row))
position = 1
page = 1

# Checks if a row exists before write
def row_exists(row):
    if height >= row:
        return True
    else:
        return False

# Draws the items currently displayed in the scroll box
def draw_scroll_box():
    for i in range(1 + (max_row * (page - 1)), max_row + 1 + (max_row * (page - 1))):
        if row_num == 0:
            box.addstr(1, 1, "No items found" + search_string,  highlightText)
        else:
            if (i + (max_row * (page - 1)) == position + (max_row * (page - 1))):
                if len(strings) > i - 1:
                    line_string = str(i) + ": " + str(strings[i - 1]) + " " * width
                    if row_exists(i - (max_row * (page - 1)) + 4):
                        box.addstr(i - (max_row * (page - 1)), 2, line_string[0:width - 5], highlightText)
            else:
                if len(strings) > i - 1:
                    line_string = str(i) + ": " + str(strings[i - 1]) + " " * width
                    if row_exists(i - (max_row * (page - 1)) + 4):
                        box.addstr(i - (max_row * (page - 1)), 2, line_string[0:width - 5], normalText)
            if i >= row_num and i <= len(strings):
                box.clrtobot()
                box.border(0)
                break
            if i == row_num:
                break

# Applies the message box in the correct 
def message_box_apply(message):
    global message_box_message
    message_box_message = message

# Draws the message box
def draw_message_box():
    if row_exists(max_row + 6):
        message_extended = message_box_message + " " * width
        message_box.addstr(1, 1, message_extended[0: width - 5])

# Draws the player status area
def draw_player_status(station, station_id, station_url, volume, status, mute):
    if  row_exists(max_row + 8):
        station_fill = "Station: " + station + " " * width
        screen.addstr(max_row + 6, 2, station_fill[0:width - 3])

    if row_exists(max_row + 9):
        station_id_fill = "Station ID: " + station_id + " " * width
        screen.addstr(max_row + 7, 2, station_id_fill[0:width - 3])

    if row_exists(max_row + 10):
        station_url_fill = "Station URL: " + station_url + " " * width
        screen.addstr(max_row + 8, 2, station_url_fill[0:width - 3])

    if row_exists(max_row + 11):
        volume_fill = "Volume: " + str(volume) + " " * width
        screen.addstr(max_row + 9, 2, volume_fill[0:width - 3])

    if row_exists(max_row + 12):
        status_fill = "Status: " + status + " " * width
        screen.addstr(max_row + 10, 2, status_fill[0:width - 3])

    if row_exists(max_row + 13):
        mute_fill = "Mute: " + mute + " " * width
        screen.addstr(max_row + 11, 2, mute_fill[0:width - 3])


draw_player_status(station_title, station_id, station_url, station_volume, station_playing, station_mute)
draw_scroll_box()
draw_message_box()
screen.refresh()
box.refresh()
message_box.refresh()

def get_row_end():
    if  max_row + 1 + (max_row * (page - 1))-1 < len(strings):
        return max_row + 1 + (max_row * (page - 1))-1
    else:
        return len(strings)


x = screen.getch()
while x != 27:
    height, width = screen.getmaxyx()
    
    # Scroll box controll section
    if x == curses.KEY_DOWN or x == ord("j"):
        if page == 1:
            if position < get_row_end():
                position = position + 1
            else:
                if pages > 1:
                    page = page + 1
                    position = 1 + (max_row * (page - 1))
        elif page == pages:
            if position < row_num:
                position = position + 1
        else:
            if position < max_row + (max_row * (page - 1)):
                position = position + 1
            else:
                page = page + 1
                position = 1 + (max_row * (page - 1))
    if x == curses.KEY_UP or x == ord("k"):
        if page == 1:
            if position > 1:
                position = position - 1
        else:
            if position > (1 + (max_row * (page - 1))):
                position = position - 1
            else:
                page = page - 1
                position = max_row + (max_row * (page - 1))
    if x == curses.KEY_LEFT:
        if page > 1:
            page = page - 1
            position = 1 + (max_row * (page - 1))
    if x == curses.KEY_RIGHT:
        if page < pages:
            page = page + 1
            position = (1 + (max_row * (page - 1)))

    # Play highlighted station
    if x == ord("\n") and row_num != 0:
        screen.erase()
        screen.border(0)
        station_id = str(search_item_stations[position - 1]['id'])
        station_title = str(search_item_stations[position - 1]['name'])
        station_info: dict = sc.station_info(station_id)
        locations_list = station_info['locations']
        if len(locations_list) > 0:
            station_url = locations_list[0]
            vlc.stream_media(locations_list[0])
        else:
            station_url = "Station URL not found"
        station_playing = vlc.get_play()
    
    # Save highlighted station to favorites
    if x == ord("s") and row_num != 0:
        screen.erase()
        screen.border(0)
        save_id = str(search_item_stations[position - 1]['id'])
        save_title = str(search_item_stations[position - 1]['name'])
        favorites = user_data.get_saved_station_ids()
        current_page = page
        current_position = position
        if len(sc.station_info(save_id)['locations']) > 0:
            save_url = sc.station_info(save_id)['locations'][0]
            if int(save_id) in favorites:
                message_box_apply(f"{save_title} already added")
            else:
                station = {
                    'id': int(save_id),
                    'name': save_title
                }
                user_data.save_station(station)
                message_box_apply(f"Added {save_title} to saved stations")
                favorites = user_data.get_saved_station_ids()
                search_item_titles = list(map(lambda x: "❤ " + x['name'] if int(x['id']) in favorites else x['name'], search_item_stations))
        else:
            message_box_apply(f"Error adding {save_title}, no stream location")

        strings = search_item_titles
        row_num = len(strings)
        pages = int(ceil(row_num / max_row))
        page = current_page
        position = current_position
    
    # Remove highlighted station from favorites
    if x == ord("d") and row_num != 0:
        screen.erase()
        screen.border(0)
        remove_id = str(search_item_stations[position - 1]['id'])
        remove_title = str(search_item_stations[position - 1]['name'])
        favorites = user_data.get_saved_station_ids()
        current_page = page
        current_position = position
        if int(remove_id) not in favorites:
            message_box_apply(f"{remove_title} already removed")
        else:
            user_data.remove_station(remove_id)
            message_box_apply(f"Removed {remove_title} from saved stations")
            favorites = user_data.get_saved_station_ids()
            search_item_titles = list(map(lambda x: "❤ " + x['name'] if int(x['id']) in favorites else x['name'], search_item_stations))

        strings = search_item_titles
        row_num = len(strings)
        pages = int(ceil(row_num / max_row))
        page = current_page
        position = current_position

    # Volume up
    if x == ord("a"):
        station_volume = vlc.volume_up()
        user_data.save_volume(station_volume)

    # Volume down
    if x == ord ("z"):
        station_volume = vlc.volume_down()
        user_data.save_volume(station_volume)

    # Toggle Mute
    if x == ord ("m"):
        station_mute = vlc.toggle_mute()
    
    # Toggle pause and mute
    if x == ord (" "):
        station_playing = vlc.toggle_play()

    # Open favorites list
    if x == ord("f"):
        message_box_apply("Favorites list")
        stations = user_data.get_stations()
        favorites = list(map(lambda x: x['id'], stations))
        if len(stations) > 0:
            search_item_titles = list(map(lambda x: "❤ " + x['name'] if int(x['id']) in favorites else x['name'], stations))
            search_item_stations = stations
        else:
            search_item_titles = []
            search_item_stations = []
        strings = search_item_titles
        row_num = len(strings)
        if max_row > 0:
         pages = int(ceil(row_num / max_row))
        position = 1
        page = 1

    # Search streams
    if x == ord("/"):
        screen.erase()
        screen.border(0)
        screen.addstr(1,1, 'Search for a stream:', curses.A_BOLD)
        screen.refresh()
        screen.move(10,26)
        curses.echo()
        search_string = screen.getstr(1,22, 30).decode('utf-8')
        curses.noecho()
        search_items = sc.search(search_string)
        screen.erase()
        if "'station'" in str(search_items):
            if isinstance(search_items['response']['data']['stationlist']['station'], list):
                favorites = user_data.get_saved_station_ids()
                search_item_titles = list(map(lambda x: "❤ " + x['name'] if int(x['id']) in favorites else x['name'], search_items['response']['data']['stationlist']['station']))
                search_item_stations = search_items['response']['data']['stationlist']['station'] 
            else:
                search_item_titles = []
                search_item_stations = []
                search_item_titles.append(search_items['response']['data']['stationlist']['station']['name'])
                search_item_stations.append(search_items['response']['data']['stationlist']['station'])
        else:
            search_item_titles = []
            search_item_stations = []

        message_box_apply(f"Search results for: {search_string}")
        strings = search_item_titles
        row_num = len(strings)
        if max_row > 0:
         pages = int(ceil(row_num / max_row))
        position = 1
        page = 1

    if x == ord("q"):
        curses.endwin()
        exit()

    screen.erase()
    if height > 20:
        max_row = height - 12
    elif height < 20:
        max_row = height - 4
    box_height = max_row + 2
    if height < max_row + 2:
        box_height = height - 2
    box = curses.newwin(box_height, width - 2, 1, 1)
    if height > 20:
        message_box = curses.newwin(3, width - 2, max_row + 3, 1)
        message_box.box()
    if max_row > 0:
        pages = int(ceil(row_num / max_row))
    box.box()
    screen.border(0)
    screen.border(0)
    box.border(0)
    message_box.border(0)
    draw_scroll_box()
    if height > 20:
        draw_message_box()
        draw_player_status(station_title, station_id, station_url, station_volume, station_playing, station_mute)
    screen.refresh()
    message_box.refresh()
    box.refresh()

    x = screen.getch()

curses.endwin()
exit()
