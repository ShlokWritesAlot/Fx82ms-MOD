import time

class MCP23017Sim:
    """Simulates a matrix keypad scanner using MCP23017 I2C expander."""
    def __init__(self, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.active_row = -1
        self.matrix_state = [[False for _ in range(cols)] for _ in range(rows)]
        self.last_pressed_key = None
        self.debounce_ms = 50
        self.scan_interval = 0.01 # 10ms
        self.i2c_address = 0x20

    def press_key(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.matrix_state[row][col] = True

    def release_key(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.matrix_state[row][col] = False

    def scan(self):
        """Simulates one scan cycle."""
        detected = []
        for r in range(self.rows):
            self.active_row = r
            # In a real MCP23017, you'd pull a row LOW and read columns
            for c in range(self.cols):
                if self.matrix_state[r][c]:
                    detected.append((r, c))
            # Simulate scan time
            # time.sleep(0.001) 
        return detected

    def get_raw_state(self):
        """Returns a bitmask representation of the matrix."""
        mask = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.matrix_state[r][c]:
                    mask |= (1 << (r * self.cols + c))
        return mask
