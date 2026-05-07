import re

class OLEDRenderer:
    """Handles text formatting and pagination for the 128x32 OLED."""
    def __init__(self, cols=21, rows=4):
        self.cols = cols
        self.rows = rows

    def clean_text(self, text: str) -> str:
        # Remove markdown
        text = re.sub(r'\*\*|__|\*|_|`|#', '', text)
        # Remove bullets
        text = re.sub(r'^[\s\-\*•]+', '', text, flags=re.MULTILINE)
        # Flatten newlines
        text = text.replace('\n', ' ').replace('\r', ' ')
        return re.sub(r'\s+', ' ', text).strip()

    def wrap_text(self, text: str) -> list:
        words = text.split()
        lines = []
        current_line = []
        current_len = 0
        
        for word in words:
            if current_len + len(word) + (1 if current_line else 0) <= self.cols:
                current_line.append(word)
                current_len += len(word) + (1 if len(current_line) > 1 else 0)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_len = len(word)
        
        if current_line:
            lines.append(" ".join(current_line))
        return lines

    def paginate(self, lines: list) -> list:
        return [lines[i:i + self.rows] for i in range(0, len(lines), self.rows)]

    def format_response(self, raw_text: str):
        clean = self.clean_text(raw_text)
        lines = self.wrap_text(clean)
        pages = self.paginate(lines)
        return pages
