import curses
import curses.textpad as textpad
import curses.panel as panel
import traceback
import scroll_window as sw

scr_width = 100
scr_height = 100


def create_panel(panel_title, height, width, x_coordinate, y_coordinate):
    window_panel = curses.newwin(height, width, y_coordinate, x_coordinate)
    window_panel.erase()
    window_panel.box()
    window_panel.addstr(0, 0, panel_title)
    created_panel = panel.new_panel(window_panel)
    return window_panel, created_panel

def base_screen(stdscr):
    stdscr.box()
    stdscr.border(0)
    stdscr.addstr(5, 5, 'Hello from Curses!', curses.A_BOLD)
    stdscr.addstr(6, 5, 'Press q to close this screen', curses.A_NORMAL)

def search_screen(stdscr):
    stdscr.box()
    stdscr.border(0)
    stdscr.addstr(5, 5, 'Hello from Curses!', curses.A_BOLD)
    stdscr.addstr(6, 5, 'Press q to close this screen', curses.A_NORMAL)

def enter_is_terminate(x):
    if x == 10:
        x = 7
    return x

def main_interface(stdscr):
    try:
        # -- Initialize --
        #stdscr = curses.initscr()   # initialize curses screen
        curses.noecho()             # turn off auto echoing of keypress on to screen
        curses.cbreak()             # enter break mode where pressing Enter key
                                    #  after keystroke is not required for it to register
        stdscr.keypad(1)            # enable special Key values such as curses.KEY_LEFT etc

        # -- Perform an action with Screen --
        stdscr.box()
        stdscr.border(0)
        stdscr.addstr(1, 1, 'ShoutCurses: A Curses Shoutcast player', curses.A_BOLD)
        #stdscr.addstr(6, 5, 'Press q to close this screen', curses.A_NORMAL)
        

        while True:
            # stay in this loop till the user presses 'q'
            stdscr.refresh()
            ch = stdscr.getch()
            height, width = stdscr.getmaxyx()
            if ch == ord('q'):
                break
            if ch == ord('s'):
                stdscr.addstr(10,5, 'Search for a stream:', curses.A_BOLD)
                #window1, panel1 = create_panel('Results', 30, 50, 5, 11)
                #curses.panel.update_panels()
                stdscr.refresh()
                stdscr.move(10,26)
                #test = stdscr.getch()
                #test_text = textpad.Textbox(stdscr).edit(enter_is_terminate)
                content_test = ["content 1", "content 2", "content 3", "content 4", "content 5", "content 6", "content 7", "content 8", "content 9", "content 10", "content 11", "content 12", "content 13", "content 14", "content 15"]
                curses.echo()
                search_string = stdscr.getstr(10,26, 20)
                curses.noecho()
                stdscr.addstr(11,5, search_string, curses.A_BOLD) 
                
            if ch == ord('x'):
                stdscr.addstr(10,5, 'Search for a stream', curses.A_BOLD)
                content_test = ["content 1", "content 2", "content 3", "content 4", "content 5", "content 6", "content 7", "content 8", "content 9", "content 10", "content 11", "content 12", "content 13", "content 14", "content 15"]
                window1, panel1 = create_panel('Results', 20, width - 2, 1, 10)
                curses.panel.update_panels()  
                #x = sw.scroll_window(content_test, panel1)
                #
                # ??????????????????????????????????????????????stdscr.refresh()
                #panel1.top()
                #curses.panel.update_panels()
                #stdscr.refresh()
                #tb = curses.textpad.Textbox(window1)
                #text = tb.edit(enter_is_terminate)
                stdscr.refresh()
            # stdscr.attron(curses.color_pair(3))
            # stdscr.addstr(height-1, 0, "status bar here")
            # stdscr.addstr(height-1, len("status bar here"), " " * (width - len("status bar here") - 1))
            # stdscr.attroff(curses.color_pair(3))
            # stdscr.refresh()
        # -- End of user code --
    except:
        traceback.print_exc()     # print trace back log of the error

    finally:
        # --- Cleanup on exit ---
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

if __name__ == '__main__':
    curses.wrapper(main_interface)
