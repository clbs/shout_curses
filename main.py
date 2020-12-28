import curses
from math import ceil
from shoutcast_data import ShoutCast
from player import VLCPlayer
from user_data import UserData
from os import getenv as getenv
import dotenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

vlc = VLCPlayer()

user_data = UserData(getenv('USER_DATA_CONFIG'))

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
box = curses.newwin(max_row + 2, width - 2, 1, 1)
message_box = curses.newwin(3, width - 2, max_row + 3, 1)
search_string = ""
message_box_message = "Welcome to Shout Curses"
message_box.box()
box.box()

station_title = ""
station_id = ""
station_url = ""


sc = ShoutCast(getenv('SHOUTCAST_API_KEY'), 'json')
# this should be removed eventually
stations = user_data.get_stations()
search_items = {}
search_item_stations = stations
favorites = user_data.get_saved_station_ids()
search_item_titles = list(map(lambda x: str("❤ " + x['name'] if int(x['id']) in favorites else x['name']), stations))
strings = search_item_titles
row_num = len(strings)

screen.addstr(26, 2, "PLAYING STATION:            ")
screen.addstr(27, 2, "STATION ID:                 ")
screen.addstr(28, 2, "STATION URL:                           ")
screen.addstr(29, 2, "Volume: " + str(vlc.player.audio_get_volume()) + "  ")
screen.addstr(30, 2, "Status: " + vlc.get_play())
screen.addstr(31, 2, vlc.get_mute())

pages = int(ceil(row_num / max_row))
position = 1
page = 1

def draw_scroll_box():
    for i in range(1 + (max_row * (page - 1)), max_row + 1 + (max_row * (page - 1))):
        if row_num == 0:
            box.addstr(1, 1, "No items found" + search_string,  highlightText)
        else:
            if (i + (max_row * (page - 1)) == position + (max_row * (page - 1))):
                line_string = str(i) + ": " + str(strings[i - 1]) + " " * width
                box.addstr(i - (max_row * (page - 1)), 2, line_string[0:width - 5], highlightText)
            else:
                line_string = str(i) + ": " + str(strings[i - 1]) + " " * width
                box.addstr(i - (max_row * (page - 1)), 2, line_string[0:width - 5], normalText)
            if i >= row_num and i <= len(strings):
                box.clrtobot()
                box.border(0)
                break
            if i == row_num:
                break

def message_box_apply(message):
    global message_box_message
    message_extended = message + " " * width
    message_box_message = message_extended[0:width -5]


def draw_message_box():
    message_box.addstr(1, 1, message_box_message)


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
    if x == curses.KEY_DOWN:
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
    if x == curses.KEY_UP:
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

    #play highlighted station
    if x == ord("\n") and row_num != 0:
        screen.erase()
        screen.border(0)
        station_id = str(search_item_stations[position - 1]['id'])
        station_title = str(search_item_stations[position - 1]['name'])
        if len(sc.station_info(station_id)['locations']) > 0:
            station_url = sc.station_info(station_id)['locations'][0]
            screen.addstr(26, 2, "PLAYING STATION: " + station_title)
            screen.addstr(27, 2, "STATION ID: " + station_id)
            screen.addstr(28, 2, "STATION URL: " + station_url)
            screen.addstr(29, 2, "Volume: " + str(vlc.player.audio_get_volume()) + "  ")
            vlc.stream_media(sc.station_info(station_id)['locations'][0])
        else:
            screen.addstr(26, 2, "PLAYING STATION: " + station_title)
            screen.addstr(27, 2, "STATION ID: " + station_id)
            screen.addstr(28, 2, "STATION URL: " + "Station URL not found")
            screen.addstr(29, 2, "Volume: " + str(vlc.player.audio_get_volume()) + "  ")
        box = curses.newwin(max_row + 2, width - 2, 1, 1)
        message_box = curses.newwin(3, width - 2, max_row + 3, 1)
        box.box()
        message_box.box()
        screen.addstr(30, 2, "Status: " + vlc.get_play())
        screen.border(0)
        box.border(0)
        message_box.border(0)
    
    #save highlighted station to favorites
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

        box = curses.newwin(max_row + 2, width - 2, 1, 1)
        message_box = curses.newwin(3, width - 2, max_row + 3, 1)
        box.box()
        message_box.box()
        strings = search_item_titles
        row_num = len(strings)
        pages = int(ceil(row_num / max_row))
        page = current_page
        position = current_position
        draw_scroll_box()
        draw_message_box()
        screen.addstr(26, 2, "PLAYING STATION: " + station_title)
        screen.addstr(27, 2, "STATION ID: " + station_id)
        screen.addstr(28, 2, "STATION URL: " + station_url)
        screen.addstr(29, 2, "Volume: " + str(vlc.player.audio_get_volume()) + "  ")
        screen.addstr(30, 2, "Status: " + vlc.get_play())
        screen.refresh()
        box.refresh()
        message_box.refresh()
        screen.border(0)
        box.border(0)
        screen.addstr(30, 2, "Status: " + vlc.get_play())
        screen.border(0)
        box.border(0)
        message_box.border(0)
    
    # remove highlighted station from favorites
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

        box = curses.newwin(max_row + 2, width - 2, 1, 1)
        message_box = curses.newwin(3, width - 2, max_row + 3, 1)
        box.box()
        message_box.box()
        strings = search_item_titles
        row_num = len(strings)
        pages = int(ceil(row_num / max_row))
        page = current_page
        position = current_position
        draw_scroll_box()
        draw_message_box()
        screen.addstr(26, 2, "PLAYING STATION: " + station_title)
        screen.addstr(27, 2, "STATION ID: " + station_id)
        screen.addstr(28, 2, "STATION URL: " + station_url)
        screen.addstr(29, 2, "Volume: " + str(vlc.player.audio_get_volume()) + "  ")
        screen.addstr(30, 2, "Status: " + vlc.get_play())
        screen.refresh()
        box.refresh()
        message_box.refresh()
        screen.border(0)
        box.border(0)
        screen.addstr(30, 2, "Status: " + vlc.get_play())
        screen.border(0)
        box.border(0)
        message_box.border(0)

    if x == ord("a"):
        screen.addstr(29, 2, "Volume: " + vlc.volume_up() + "  ")
    if x == ord ("z"):
        screen.addstr(29, 2, "Volume: " + vlc.volume_down() + "  ")
    if x == ord ("m"):
        screen.addstr(31, 2, vlc.toggle_mute())
    if x == ord (" "):
        screen.addstr(29, 2, "Status: " + vlc.toggle_play() + "   ")
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

        box = curses.newwin(max_row + 2, width - 2, 1, 1)
        message_box = curses.newwin(3, width - 2, max_row + 3, 1)
        box.box()
        message_box.box()
        strings = search_item_titles
        row_num = len(strings)
        pages = int(ceil(row_num / max_row))
        position = 1
        page = 1
        draw_scroll_box()
        draw_message_box()
        screen.addstr(26, 2, "PLAYING STATION: " + station_title)
        screen.addstr(27, 2, "STATION ID: " + station_id)
        screen.addstr(28, 2, "STATION URL: " + station_url)
        screen.addstr(29, 2, "Volume: " + str(vlc.player.audio_get_volume()) + "  ")
        screen.addstr(30, 2, "Status: " + vlc.get_play())
        screen.refresh()
        box.refresh()
        message_box.refresh()
        screen.border(0)
        box.border(0)
        message_box.border(0)
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
        box = curses.newwin(max_row + 2, width - 2, 1, 1)
        message_box = curses.newwin(3, width - 2, max_row + 3, 1)
        box.box()
        message_box.box()
        strings = search_item_titles
        row_num = len(strings)
        pages = int(ceil(row_num / max_row))
        position = 1
        page = 1
        draw_scroll_box()
        draw_message_box()
        screen.addstr(26, 2, "PLAYING STATION: " + station_title)
        screen.addstr(27, 2, "STATION ID: " + station_id)
        screen.addstr(28, 2, "STATION URL: " + station_url)
        screen.addstr(29, 2, "Volume: " + str(vlc.player.audio_get_volume()) + "  ")
        screen.addstr(30, 2, "Status: " + vlc.get_play())
        screen.refresh()
        box.refresh()
        message_box.refresh()
        screen.border(0)
        box.border(0)
        message_box.border(0)

    draw_scroll_box()
    draw_message_box()
    screen.refresh()
    message_box.refresh()
    box.refresh()
    x = screen.getch()

curses.endwin()
exit()
