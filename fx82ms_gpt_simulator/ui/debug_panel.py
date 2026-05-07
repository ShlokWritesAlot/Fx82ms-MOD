from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QFormLayout, QTextEdit
from PySide6.QtCore import Qt

class DebugPanel(QWidget):
    """Shows simulated telemetry from ESP32, MCP23017, and API."""
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        
        layout = QVBoxLayout()
        
        # ESP32 Group
        esp_group = QGroupBox("ESP32-C3 Telemetry")
        esp_form = QFormLayout()
        self.esp_state = QLabel("BOOTING")
        self.esp_wifi = QLabel("Disconnected")
        self.esp_batt = QLabel("100%")
        self.esp_uptime = QLabel("0s")
        esp_form.addRow("State:", self.esp_state)
        esp_form.addRow("WiFi:", self.esp_wifi)
        esp_form.addRow("Battery:", self.esp_batt)
        esp_form.addRow("Uptime:", self.esp_uptime)
        esp_group.setLayout(esp_form)
        layout.addWidget(esp_group)
        
        # MCP23017 Group
        mcp_group = QGroupBox("MCP23017 Matrix")
        mcp_form = QFormLayout()
        self.mcp_active_row = QLabel("-1")
        self.mcp_detected = QLabel("None")
        self.mcp_raw = QLabel("0x00")
        mcp_form.addRow("Active Row:", self.mcp_active_row)
        mcp_form.addRow("Detected:", self.mcp_detected)
        mcp_form.addRow("Raw Bits:", self.mcp_raw)
        mcp_group.setLayout(mcp_form)
        layout.addWidget(mcp_group)
        
        # API Log
        api_group = QGroupBox("API Log")
        api_layout = QVBoxLayout()
        self.api_log = QTextEdit()
        self.api_log.setReadOnly(True)
        self.api_log.setFontPointSize(8)
        api_layout.addWidget(self.api_log)
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        self.setLayout(layout)

    def log_api(self, msg):
        self.api_log.append(f"> {msg}")
        # Scroll to bottom
        self.api_log.verticalScrollBar().setValue(
            self.api_log.verticalScrollBar().maximum()
        )

    def update_telemetry(self, esp, mcp):
        self.esp_state.setText(esp.state.name)
        self.esp_wifi.setText("Connected" if esp.wifi_connected else "Disconnected")
        self.esp_batt.setText(f"{esp.battery_level:.1f}%")
        self.esp_uptime.setText(f"{esp.uptime}s")
        
        self.mcp_active_row.setText(str(mcp.active_row))
        self.mcp_raw.setText(hex(mcp.get_raw_state()))
