import curses
import time

SIZE = 10
DIRS = [-SIZE - 1, -SIZE, -SIZE + 1, -1, 1, SIZE - 1, SIZE, SIZE + 1]

def index_for(x, y):
    return y * SIZE + x

def coords_for(i):
    return (i % SIZE, i // SIZE)

def possible_moves(board, player):
    result = set()
    for i in range(len(board)):
        if board[i] == player:
            for d in DIRS:
                pos = i + d
                legal = False
                while board[pos] == -player:
                    legal = True
                    pos += d
                if legal and board[pos] == 0:
                    result.add(pos)
    return result

def apply_move(board, move, player):
    board[move] = player
    for d in DIRS:
        p = move + d
        flips = set()
        while board[p] == -player:
            flips.add(p)
            p += d
        if board[p] == player:
            for f in flips:
                board[f] = player

def init_curses(scr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)

def show_board(scr, board):
    for x in range(SIZE):
        for y in range(SIZE):
            v = board[index_for(x, y)]
            c = "?"
            if v == 0:
                c = "."
            elif v == 1:
                c = "X"
            elif v == -1:
                c = "O"
            elif v == 9:
                c = "#"
            scr.addstr(y, x, c)
    scr.refresh()

def show_moves(scr, moves):
    scr.attron(curses.color_pair(1))
    for m in moves:
        x, y = coords_for(m)
        scr.addstr(y, x, "*")
    scr.attroff(curses.color_pair(1))
    scr.refresh()

def highlight_move(scr, m):
    x, y = coords_for(m)
    scr.attron(curses.color_pair(2))
    scr.addstr(y, x, "*")
    scr.attroff(curses.color_pair(2))
    scr.refresh()
    #time.sleep(0.5)
    scr.getch()

def main(scr):
    init_curses(scr)
    board = [0] * SIZE * SIZE
    for i in range(SIZE):
        board[index_for(0, i)] = 9
        board[index_for(SIZE - 1, i)] = 9
        board[index_for(i, 0)] = 9
        board[index_for(i, SIZE - 1)] = 9
    board[index_for(SIZE // 2 - 1, SIZE // 2 - 1)] = 1
    board[index_for(SIZE // 2, SIZE // 2 - 1)] = -1
    board[index_for(SIZE // 2 - 1, SIZE // 2)] = -1
    board[index_for(SIZE // 2, SIZE // 2)] = 1

    active_player = 1
    pieces = [32, 0, 32]
    game_running = True
    previous_player_passed = False
    while game_running:
        show_board(scr, board)
        if pieces[active_player + 1] > 0:
            moves = possible_moves(board, active_player)
        else:
            moves = set()
        show_moves(scr, moves)
        if len(moves) > 0:
            move = moves.pop()
            highlight_move(scr, move)
            apply_move(board, move, active_player)
            pieces[active_player + 1] -= 1
            previous_player_passed = False
            scr.addstr(1, 12, "       ")
            scr.refresh()
        else:
            if previous_player_passed:
                game_running = False
            else:
                scr.addstr(1, 12, "Passed!")
                scr.refresh()
                time.sleep(0.5)
                previous_player_passed = True
        active_player *= -1

curses.wrapper(main)
