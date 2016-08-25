import curses

stdscr = curses.initscr()

curses.start_color()
#curses.noecho()

i = 0
j = 0
k = 1

try:
    while j < 256:
        curses.init_pair(k, 255 - j, j)
        stdscr.addstr(str(j) + ' ', curses.color_pair(k))
        stdscr.addstr(' ')
        j += 1
        k += 1
    stdscr.getch()
    i = 0
    j = 0
    k = 1
    stdscr.move(0,0)
    while j < 256:
        curses.init_pair(k, j, j)
        stdscr.addstr(str(j) + ' ', curses.color_pair(k))
        stdscr.addstr(' ')
        j += 1
        k += 1
    stdscr.getch()
    # i = 0
    # j = 0
    # k = 1
    # while i < 256:
    #     curses.init_pair(k, i, 0)
    #     stdscr.addstr('A', curses.color_pair(k))
    #     i += 1
    #     k += 1
    # stdscr.getch()

    # while j < 256:
    #     curses.init_pair(k, i, j)
    #     stdscr.addstr(str(i) + str(j), curses.color_pair(k))
    #     j += 1
    #     k += 1
    # #stdscr.getch()
    #
    # while i < 256:
    #     stdscr.getch()
    #     i += 1
    #     j = 0
    #     k =1
    #     while j < 256:
    #         curses.init_pair(k, i, j)
    #         j += 1
    #         k += 1
    # stdscr.getch()

finally:
    #curses.echo()
    curses.endwin()


# while j < 256:
#         curses.init_pair(k, j, 255 - j)
#         stdscr.addstr(str(j) + ' ' + str(255 - j), curses.color_pair(k))
#         stdscr.addstr(' ')
#         j += 1
#         k += 1
#     stdscr.getch()