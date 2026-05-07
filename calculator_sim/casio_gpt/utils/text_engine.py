from ..config import settings

class TextEngine:
    """Utilities for fitting text into the tiny OLED display."""
    
    @staticmethod
    def wrap_text(text: str, width: int = settings.SCREEN_COLS) -> list:
        """Wraps text into lines that fit the width."""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + (1 if current_line else 0) <= width:
                current_line.append(word)
                current_length += len(word) + (1 if len(current_line) > 1 else 0)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(" ".join(current_line))
            
        return lines

    @staticmethod
    def paginate(lines: list, page_size: int = settings.SCREEN_ROWS) -> list:
        """Splits lines into pages."""
        return [lines[i:i + page_size] for i in range(0, len(lines), page_size)]
