import os
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import QTimer, Qt, Signal
from ui.calculator_view import CalculatorView
from ui.oled_view import OLEDView
from ui.debug_panel import DebugPanel
from ui.styles import DARK_THEME
from core.esp32_sim import ESP32Sim, ESP32State
from core.mcp23017_sim import MCP23017Sim
from api.ai_client import AIClient
from rendering.oled_renderer import OLEDRenderer
from ai.prompt_builder import PromptBuilder
from input.multitap_handler import MultiTapHandler, InputMode
from ui.debug_window import DebugWindow

class MainWindow(QMainWindow):
    ai_response_received = Signal(dict)

    def __init__(self):
        super().__init__()
        # Standard 96 PPI dimensions (77mm x 161.5mm) = 291px x 610px
        self.setFixedSize(291, 610)
        self.setWindowTitle("Casio fx-82MS GPT")
        self.setStyleSheet(DARK_THEME)
        
        # Core Simulations
        self.esp32 = ESP32Sim()
        self.mcp = MCP23017Sim()
        self.api = AIClient()
        self.renderer = OLEDRenderer()
        
        # New Hardware Logic
        templates_path = os.path.join(os.path.dirname(__file__), "..", "config", "prompt_templates.json")
        self.prompt_builder = PromptBuilder(templates_path)
        self.multitap = MultiTapHandler()
        
        # Separate Debug Console
        self.debug_window = DebugWindow(self.esp32, self.mcp)
        self.debug_window.show()
        
        # State
        self.gpt_menu_options = ["DEFINE", "EXPLAIN", "SOLVE", "FORMULA", "CONVERT", "FREE_ASK"]
        self.selected_menu_idx = 0
        self.selected_mode = "FREE_ASK"
        self.input_buffer = ""
        self.ai_pages = []
        self.current_page = 0
        
        # Connect signals
        self.ai_response_received.connect(self.handle_ai_response)
        self.multitap.char_committed.connect(self.on_char_committed)
        self.multitap.buffer_updated.connect(self.on_multitap_update)
        
        self.init_ui()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(100)
        
        self.boot()

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Main Shell
        shell = QWidget()
        shell.setObjectName("calculator_shell")
        shell.setStyleSheet("#calculator_shell { background-color: #37474f; border-radius: 40px; }")
        
        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(10, 30, 10, 20)
        shell_layout.setSpacing(15)
        
        # Branding
        header = QHBoxLayout()
        casio_lbl = QLabel("CASIO")
        casio_lbl.setStyleSheet("color: white; font-weight: bold; font-size: 22px; font-family: Arial; margin-left: 15px;")
        header.addWidget(casio_lbl)
        header.addStretch()
        model_lbl = QLabel("fx-82MS")
        model_lbl.setStyleSheet("color: white; font-size: 14px; font-family: Arial; margin-right: 15px;")
        header.addWidget(model_lbl)
        shell_layout.addLayout(header)

        # Original Large Display Cutout (Housing for the OLED)
        display_housing = QFrame()
        display_housing.setObjectName("display_housing")
        display_housing.setFixedSize(227, 68)
        display_housing.setStyleSheet("""
            #display_housing {
                background-color: #1a1a1a;
                border: 4px solid #101010;
                border-radius: 5px;
            }
        """)
        
        housing_layout = QVBoxLayout(display_housing)
        housing_layout.setContentsMargins(0, 0, 0, 0)
        
        # The 0.91" OLED Module inside the housing
        self.oled = OLEDView()
        housing_layout.addWidget(self.oled, alignment=Qt.AlignCenter)
        
        shell_layout.addWidget(display_housing, alignment=Qt.AlignCenter)
        
        # Keypad
        keymap_path = os.path.join(os.path.dirname(__file__), "..", "config", "keymap_fx82ms.json")
        self.calc_view = CalculatorView(keymap_path)
        self.calc_view.key_pressed.connect(self.on_key_pressed)
        shell_layout.addWidget(self.calc_view)
        
        layout.addWidget(shell)
        central.setLayout(layout)
        self.setCentralWidget(central)

    def boot(self):
        self.esp32.set_state(ESP32State.BOOTING)
        self.oled.update_display(["", "  CASIO COMPUTER", "   INITIALIZING", ""])
        
        def check_wifi():
            result = self.api.ask("health_check") # We can use /health endpoint actually
            # Let's check health directly
            try:
                import requests
                r = requests.get("http://localhost:8001/health", timeout=1)
                if r.status_code == 200:
                    self.esp32.connect_wifi()
                    self.debug_window.log_api("WiFi Connected to Bridge")
            except:
                pass
            self.esp32.set_state(ESP32State.IDLE)
            self.show_main_menu()
            
        QTimer.singleShot(1500, check_wifi)

    def show_main_menu(self):
        self.oled.update_display(["", "   CASIO fx-82MS", "  [ALPHA]=GPT", "  [ON]=CALC"])

    def show_gpt_menu(self):
        self.esp32.set_state(ESP32State.GPT_MENU)
        
        # Add scroll indicators if not at boundaries (though it wraps, indicators help orient)
        header = "GPT MENU (1-6)"
        if self.selected_menu_idx > 0:
            header += " ^"
        if self.selected_menu_idx < len(self.gpt_menu_options) - 1:
            header += " v"
            
        display_lines = [header]
        # Show a window of 3 options
        start = self.selected_menu_idx
        for i in range(3):
            idx = (start + i) % len(self.gpt_menu_options)
            prefix = f"{idx+1}.>" if i == 0 else f"{idx+1}. "
            display_lines.append(f"{prefix}{self.gpt_menu_options[idx]}")
        self.oled.update_display(display_lines)

    def show_text_entry(self):
        self.esp32.set_state(ESP32State.TEXT_ENTRY)
        self.update_entry_screen()

    def update_entry_screen(self, pending=""):
        if self.esp32.state not in [ESP32State.TEXT_ENTRY, ESP32State.MULTITAP_PENDING]:
            return
            
        mode_str = self.multitap.mode
        # Show prompt on line 1, buffer on line 2
        line1 = f"{self.selected_mode} ({mode_str})"
        line2 = f"{self.input_buffer}{pending}_"
        # Wrap line 2 if it's long
        wrapped = self.renderer.wrap_text(line2)
        if len(wrapped) == 0: wrapped = ["_"]
        
        display_lines = [line1] + wrapped[:2] + ["=SEND DEL=BK AC=MENU"]
        self.oled.update_display(display_lines)

    def on_char_committed(self, char):
        self.input_buffer += char
        self.update_entry_screen()

    def on_multitap_update(self, pending):
        if pending:
            self.esp32.set_state(ESP32State.MULTITAP_PENDING)
        else:
            self.esp32.set_state(ESP32State.TEXT_ENTRY)
        self.update_entry_screen(pending)

    def on_key_pressed(self, key_info):
        label = key_info['label']
        row, col = key_info['row'], key_info['col']
        
        self.mcp.press_key(row, col)
        QTimer.singleShot(50, lambda: self.mcp.release_key(row, col))
        self.debug_window.panel.mcp_detected.setText(label)
        
        if label == "ON":
            self.esp32.set_state(ESP32State.IDLE)
            self.input_buffer = ""
            self.show_main_menu()
            return

        if self.esp32.state == ESP32State.IDLE:
            if label == "ALPHA" or label == "MODE":
                self.show_gpt_menu()

        elif self.esp32.state == ESP32State.GPT_MENU:
            if label == "UP":
                self.selected_menu_idx = (self.selected_menu_idx - 1) % len(self.gpt_menu_options)
                self.show_gpt_menu()
            elif label == "DOWN":
                self.selected_menu_idx = (self.selected_menu_idx + 1) % len(self.gpt_menu_options)
                self.show_gpt_menu()
            elif label.isdigit() and 1 <= int(label) <= 6:
                self.selected_menu_idx = int(label) - 1
                self.selected_mode = self.gpt_menu_options[self.selected_menu_idx]
                self.input_buffer = ""
                self.show_text_entry()
            elif label == "=" or label == "RIGHT":
                self.selected_mode = self.gpt_menu_options[self.selected_menu_idx]
                self.input_buffer = ""
                self.show_text_entry()
            elif label == "AC" or label == "BACK":
                self.esp32.set_state(ESP32State.IDLE)
                self.show_main_menu()

        elif self.esp32.state in [ESP32State.TEXT_ENTRY, ESP32State.MULTITAP_PENDING]:
            if label.isdigit() or label == ".":
                self.multitap.handle_key(label)
            elif label == "ALPHA":
                self.multitap.toggle_mode()
                self.update_entry_screen()
            elif label == "SHIFT":
                self.multitap.toggle_case()
                self.update_entry_screen()
            elif label == "DEL":
                self.input_buffer = self.input_buffer[:-1]
                self.update_entry_screen()
            elif label == "AC":
                self.show_gpt_menu()
            elif label == "=":
                self.multitap.commit()
                self.send_to_ai()

        elif self.esp32.state == ESP32State.DISPLAYING_RESPONSE:
            if label == "RIGHT" or label == "DOWN" or label == "Ans":
                self.current_page = (self.current_page + 1) % len(self.ai_pages)
                self.oled.update_display(self.ai_pages[self.current_page])
                # Show indicator on debug console
                self.debug_window.log_api(f"Paging: {self.current_page+1}/{len(self.ai_pages)}")
            elif label == "AC" or label == "BACK" or label == "LEFT":
                self.show_gpt_menu()

    def keyPressEvent(self, event):
        if self.esp32.state == ESP32State.WAITING_FOR_AI: return

        key = event.text()
        if self.esp32.state in [ESP32State.TEXT_ENTRY, ESP32State.MULTITAP_PENDING]:
            if event.key() == Qt.Key_Backspace:
                self.input_buffer = self.input_buffer[:-1]
                self.update_entry_screen()
            elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                if self.input_buffer: self.send_to_ai()
            elif event.key() >= Qt.Key_0 and event.key() <= Qt.Key_9:
                self.multitap.handle_key(key)
            elif key and key.isprintable():
                self.input_buffer += key
                self.update_entry_screen()
        else:
            super().keyPressEvent(event)

    def send_to_ai(self):
        if not self.input_buffer: return
        final_prompt = self.prompt_builder.build(self.selected_mode, self.input_buffer)
        self.esp32.set_state(ESP32State.WAITING_FOR_AI)
        self.oled.update_display(["", "   AI IS THINKING", "    PLEASE WAIT", "      ..."])
        self.debug_window.log_api(f"Final Prompt: {final_prompt}")
        
        from threading import Thread
        def run_request():
            result = self.api.ask(final_prompt)
            self.ai_response_received.emit(result)
        Thread(target=run_request, daemon=True).start()

    def handle_ai_response(self, result):
        if result['success']:
            answer = result['answer']
            self.debug_window.log_api(f"Response: {answer}")
            self.ai_pages = self.renderer.format_response(answer)
            self.current_page = 0
            self.esp32.set_state(ESP32State.DISPLAYING_RESPONSE)
            # Show "RIGHT=MORE" if multiple pages
            p1 = self.ai_pages[0]
            if len(self.ai_pages) > 1:
                p1 = p1[:3] + ["      [NEXT] >"]
            self.oled.update_display(p1)
        else:
            self.debug_window.log_api(f"Error: {result['error']}")
            self.esp32.set_state(ESP32State.ERROR)
            self.oled.update_display(["!! API OFFLINE !!", "Check Bridge", "", "Press AC"])

    def tick(self):
        self.esp32.update()
        self.mcp.scan()
        self.debug_window.update()
        
        # Periodic WiFi check if disconnected
        if not self.esp32.wifi_connected and self.esp32.uptime % 10 == 0:
            try:
                import requests
                r = requests.get("http://localhost:8001/health", timeout=0.5)
                if r.status_code == 200:
                    self.esp32.connect_wifi()
            except:
                pass
