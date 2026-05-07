import curses
import asyncio
import time
from .rendering.oled import OLEDRenderer
from .input.handler import InputHandler
from .screens.splash import SplashScreen
from .screens.menu import MenuScreen
from .screens.ask_ai import AskAIScreen

class CasioGPTSimulator:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.renderer = OLEDRenderer(stdscr)
        self.current_screen = SplashScreen(self.renderer)
        self.running = True

    async def run(self):
        # Hide cursor
        try:
            curses.curs_set(0)
        except:
            pass
            
        while self.running:
            # 1. Handle Input
            key = self.renderer.get_input()
            if key != -1:
                event = InputHandler.get_event(key)
                if event:
                    result = self.current_screen.handle_input(event)
                    self.process_screen_result(result)

            # 2. Update logic
            self.current_screen.update()
            
            # 3. Transition if needed
            if isinstance(self.current_screen, SplashScreen) and self.current_screen.finished:
                self.current_screen = MenuScreen(self.renderer)

            # 4. Render
            self.current_screen.render()
            
            # 5. Sleep to control FPS and allow async tasks
            await asyncio.sleep(0.05)

    def process_screen_result(self, result):
        if not result:
            return

        if isinstance(self.current_screen, MenuScreen):
            if result == "1.Ask AI":
                self.current_screen = AskAIScreen(self.renderer)
            elif result == "6.System Info":
                # Mock system info screen
                pass
        
        elif isinstance(self.current_screen, AskAIScreen):
            if result == "BACK":
                self.current_screen = MenuScreen(self.renderer)

def main():
    async def start_app(stdscr):
        app = CasioGPTSimulator(stdscr)
        await app.run()

    try:
        curses.wrapper(lambda stdscr: asyncio.run(start_app(stdscr)))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
