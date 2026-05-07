from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ui.debug_panel import DebugPanel

class DebugWindow(QMainWindow):
    """A separate window for telemetry and API logs to keep the main view clean."""
    def __init__(self, esp32, mcp):
        super().__init__()
        self.setWindowTitle("Casio GPT - Debug Console")
        self.setFixedSize(400, 600)
        
        self.esp32 = esp32
        self.mcp = mcp
        
        central = QWidget()
        layout = QVBoxLayout()
        
        self.panel = DebugPanel()
        layout.addWidget(self.panel)
        
        central.setLayout(layout)
        self.setCentralWidget(central)

    def update(self):
        self.panel.update_telemetry(self.esp32, self.mcp)

    def log_api(self, msg):
        self.panel.log_api(msg)
