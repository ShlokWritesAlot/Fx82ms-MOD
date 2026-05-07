import curses
from ..config import settings

class OLEDRenderer:
    """Simulates the 128x32 OLED screen in the terminal."""
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.rows = settings.SCREEN_ROWS
        self.cols = settings.SCREEN_COLS
        self.buffer = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Create a window for the OLED
        # Center it roughly
        sh, sw = stdscr.getmaxyx()
        self.win = curses.newwin(self.rows + 2, self.cols + 2, sh//2 - 2, sw//2 - 10)
        self.win.timeout(100) # Non-blocking input

    def clear(self):
        self.buffer = [[" " for _ in range(self.cols)] for _ in range(self.rows)]

    def write_line(self, row, text):
        if 0 <= row < self.rows:
            # Truncate text to fit cols
            text = text[:self.cols]
            # Update buffer
            for i, char in enumerate(text):
                self.buffer[row][i] = char
            # Fill remaining with spaces
            for i in range(len(text), self.cols):
                self.buffer[row][i] = " "

    def refresh(self):
        self.win.clear()
        self.win.box()
        for r in range(self.rows):
            line = "".join(self.buffer[r])
            self.win.addstr(r + 1, 1, line)
        self.win.refresh()

    def get_input(self):
        return self.win.getch()
