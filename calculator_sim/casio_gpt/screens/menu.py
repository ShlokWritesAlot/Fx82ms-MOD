from .base import BaseScreen
from ..config import settings

class MenuScreen(BaseScreen):
    """Main menu of the calculator."""
    
    def __init__(self, renderer):
        super().__init__(renderer)
        self.options = [
            "1.Ask AI",
            "2.Math Solver",
            "3.Definitions",
            "4.Converter",
            "5.Settings",
            "6.System Info"
        ]
        self.selected_index = 0
        self.scroll_offset = 0

    def handle_input(self, event):
        # Normalize event
        e_val = event
        if isinstance(event, tuple):
            # In Menu, BOTH always means navigation
            if event[0] == 'BOTH':
                e_val = event[1]
            else:
                e_val = event[1]

        if e_val == 'UP':
            self.selected_index = max(0, self.selected_index - 1)
            if self.selected_index < self.scroll_offset:
                self.scroll_offset = self.selected_index
        elif e_val == 'DOWN':
            self.selected_index = min(len(self.options) - 1, self.selected_index + 1)
            if self.selected_index >= self.scroll_offset + settings.SCREEN_ROWS:
                self.scroll_offset = self.selected_index - settings.SCREEN_ROWS + 1
        elif e_val == 'ENTER':
            return self.options[self.selected_index]
        return None

    def update(self):
        pass

    def render(self):
        self.renderer.clear()
        for i in range(settings.SCREEN_ROWS):
            idx = i + self.scroll_offset
            if idx < len(self.options):
                prefix = ">" if idx == self.selected_index else " "
                self.renderer.write_line(i, f"{prefix}{self.options[idx]}")
        self.renderer.refresh()
