from PySide6.QtCore import QObject, Signal, QTimer

class InputMode:
    ABC = "ABC" # Uppercase
    abc = "abc" # Lowercase
    NUM = "NUM" # Numbers

class MultiTapHandler(QObject):
    """Handles phone-style T9/Multi-tap typing logic."""
    char_committed = Signal(str) # Emitted when a character is finalized
    buffer_updated = Signal(str) # Emitted when the current pending char changes

    def __init__(self):
        super().__init__()
        self.mode = InputMode.ABC
        self.current_key = None
        self.cycle_index = -1
        self.pending_char = ""
        
        # Multi-tap mappings
        self.layout = {
            "1": ".,@#1",
            "2": "ABC2",
            "3": "DEF3",
            "4": "GHI4",
            "5": "JKL5",
            "6": "MNO6",
            "7": "PQRS7",
            "8": "TUV8",
            "9": "WXYZ9",
            "0": " 0",
            ".": ".,?!."
        }
        
        # Commit timer (0.8 seconds)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.commit)

    def handle_key(self, key: str):
        """Processes a number key press."""
        if self.mode == InputMode.NUM:
            self.char_committed.emit(key)
            return

        if key not in self.layout:
            return

        # If same key is pressed, cycle characters
        if key == self.current_key:
            self.cycle_index = (self.cycle_index + 1) % len(self.layout[key])
        else:
            # Commit previous pending char if any
            if self.current_key:
                self.commit()
            
            self.current_key = key
            self.cycle_index = 0

        # Get char based on mode
        chars = self.layout[key]
        char = chars[self.cycle_index]
        
        if self.mode == InputMode.abc and char.isalpha():
            char = char.lower()
            
        self.pending_char = char
        self.buffer_updated.emit(self.pending_char)
        
        # Reset commit timer
        self.timer.start(800)

    def commit(self):
        """Finalizes the current pending character."""
        if self.pending_char:
            self.char_committed.emit(self.pending_char)
            self.pending_char = ""
            self.current_key = None
            self.cycle_index = -1
            self.buffer_updated.emit("")

    def toggle_mode(self):
        """Cycles through ABC -> abc -> NUM."""
        if self.mode == InputMode.ABC:
            self.mode = InputMode.abc
        elif self.mode == InputMode.abc:
            self.mode = InputMode.NUM
        else:
            self.mode = InputMode.ABC
        return self.mode

    def toggle_case(self):
        """Quick toggle between ABC and abc."""
        if self.mode == InputMode.ABC:
            self.mode = InputMode.abc
        else:
            self.mode = InputMode.ABC
        return self.mode
