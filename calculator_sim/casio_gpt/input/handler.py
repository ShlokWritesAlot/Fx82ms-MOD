import curses

class InputHandler:
    """Maps terminal keyboard events to calculator button events."""
    
    KEY_MAP = {
        ord('w'): 'UP',
        ord('W'): 'UP',
        curses.KEY_UP: 'UP',
        
        ord('s'): 'DOWN',
        ord('S'): 'DOWN',
        curses.KEY_DOWN: 'DOWN',
        
        ord('a'): 'LEFT',
        ord('A'): 'LEFT',
        curses.KEY_LEFT: 'LEFT',
        
        ord('d'): 'RIGHT',
        ord('D'): 'RIGHT',
        curses.KEY_RIGHT: 'RIGHT',
        
        10: 'ENTER',    # Enter key
        13: 'ENTER',    # Carriage return
        
        27: 'BACK',     # ESC key
        ord('q'): 'BACK',
        
        curses.KEY_BACKSPACE: 'DEL',
        8: 'DEL',       # Backspace on some systems
        127: 'DEL',     # Backspace on others
        
        ord(' '): 'PAGE' # Space for pagination
    }

    @staticmethod
    def get_event(key):
        # 1. Check if it's a printable character
        char = chr(key) if 32 <= key <= 126 else None
        
        # 2. Get the mapped event
        event = InputHandler.KEY_MAP.get(key)
        
        # 3. Return based on what we found
        if event and char:
            return ('BOTH', event, char)
        if event:
            return event
        if char:
            return ('CHAR', char)
            
        return None
