import asyncio
from .base import BaseScreen
from ..config import settings

class SplashScreen(BaseScreen):
    """Startup splash screen."""
    
    def __init__(self, renderer):
        super().__init__(renderer)
        self.frame = 0
        self.max_frames = 20
        self.finished = False

    def handle_input(self, event):
        e_val = event[1] if isinstance(event, tuple) else event
        if e_val == 'ENTER':
            self.finished = True
        return None

    def update(self):
        self.frame += 1
        if self.frame >= self.max_frames:
            self.finished = True

    def render(self):
        self.renderer.clear()
        if self.frame < 5:
            self.renderer.write_line(1, "  CASIO COMPUTER")
        elif self.frame < 12:
            self.renderer.write_line(1, "   CASIO fx-82MS")
            self.renderer.write_line(2, "   MOD BY SHLOK")
        else:
            self.renderer.write_line(1, "   INITIALIZING")
            # Progress bar
            progress = (self.frame - 12) * 2
            bar = "[" + "=" * progress + " " * (16 - progress) + "]"
            self.renderer.write_line(2, bar[:settings.SCREEN_COLS])
            
        self.renderer.refresh()
