import asyncio
from .base import BaseScreen
from ..config import settings
from ..api.client import APIClient
from ..utils.text_engine import TextEngine

class AskAIScreen(BaseScreen):
    """Screen for asking AI questions."""
    
    def __init__(self, renderer):
        super().__init__(renderer)
        self.state = "INPUT" # INPUT, LOADING, RESPONSE, ERROR
        self.prompt = ""
        self.response = ""
        self.pages = []
        self.current_page = 0
        self.api_client = APIClient()
        self.loading_frame = 0
        self.error_msg = ""

    def handle_input(self, event):
        # Normalize event
        e_type = None
        e_val = None
        
        if isinstance(event, tuple):
            e_type = event[0]
            if e_type == 'BOTH':
                # In INPUT mode, BOTH behaves like CHAR
                # In RESPONSE mode, BOTH behaves like EVENT
                if self.state == "INPUT":
                    e_type = 'CHAR'
                    e_val = event[2] # char
                else:
                    e_type = 'EVENT'
                    e_val = event[1] # event
            else:
                e_val = event[1]
        else:
            e_type = 'EVENT'
            e_val = event

        if self.state == "INPUT":
            if e_type == 'CHAR':
                if len(self.prompt) < 50:
                    self.prompt += e_val
            elif e_val == 'DEL':
                self.prompt = self.prompt[:-1]
            elif e_val == 'ENTER' and self.prompt:
                self.state = "LOADING"
                asyncio.create_task(self.fetch_response())
            elif e_val == 'BACK':
                return "BACK"
        
        elif self.state == "RESPONSE":
            if e_val == 'PAGE' or e_val == 'DOWN':
                if self.current_page < len(self.pages) - 1:
                    self.current_page += 1
                else:
                    self.state = "INPUT"
                    self.prompt = ""
            elif e_val == 'UP':
                self.current_page = max(0, self.current_page - 1)
            elif e_val == 'BACK':
                self.state = "INPUT"
                self.prompt = ""

        elif self.state == "ERROR":
            if e_val == 'ENTER' or e_val == 'BACK':
                self.state = "INPUT"
        
        return None

    async def fetch_response(self):
        result = await self.api_client.ask_ai(self.prompt)
        if result["success"]:
            self.response = result["answer"]
            lines = TextEngine.wrap_text(self.response)
            self.pages = TextEngine.paginate(lines)
            self.current_page = 0
            self.state = "RESPONSE"
        else:
            self.error_msg = result["error"]
            self.state = "ERROR"

    def update(self):
        if self.state == "LOADING":
            self.loading_frame = (self.loading_frame + 1) % 4

    def render(self):
        self.renderer.clear()
        
        if self.state == "INPUT":
            self.renderer.write_line(0, "ASK AI:")
            # Show prompt with cursor
            display_prompt = self.prompt + "_"
            # Wrap prompt for display
            lines = TextEngine.wrap_text(display_prompt, settings.SCREEN_COLS)
            for i, line in enumerate(lines[:3]):
                self.renderer.write_line(i + 1, line)
                
        elif self.state == "LOADING":
            self.renderer.write_line(1, "  Thinking...")
            spinner = ["|", "/", "-", "\\"]
            self.renderer.write_line(2, f"      {spinner[self.loading_frame]}")
            
        elif self.state == "RESPONSE":
            page = self.pages[self.current_page]
            for i, line in enumerate(page):
                self.renderer.write_line(i, line)
            # Progress indicator on bottom right if multiple pages
            if len(self.pages) > 1:
                prog = f"{self.current_page+1}/{len(self.pages)}"
                # We can't really do "bottom right" easily with write_line, but we can append to last line
                # or just use a dedicated line if there's space.
                # Let's just keep it simple.
                pass

        elif self.state == "ERROR":
            self.renderer.write_line(0, "!! ERROR !!")
            self.renderer.write_line(1, self.error_msg[:settings.SCREEN_COLS])
            self.renderer.write_line(3, "Press ENTER")
            
        self.renderer.refresh()
