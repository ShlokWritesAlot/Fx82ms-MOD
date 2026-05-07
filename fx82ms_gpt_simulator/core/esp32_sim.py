from enum import Enum, auto
import time

class ESP32State(Enum):
    BOOTING = auto()
    IDLE = auto()
    GPT_MENU = auto()             # New: Mode selection (Define, Explain, etc)
    TEXT_ENTRY = auto()           # New: Typing the keyword/equation
    MULTITAP_PENDING = auto()     # New: Waiting for character commit
    SENDING_REQUEST = auto()
    WAITING_FOR_AI = auto()
    DISPLAYING_RESPONSE = auto()
    ERROR = auto()
    LOW_BATTERY = auto()
    SLEEP = auto()

class ESP32Sim:
    """Simulates the ESP32-C3 firmware state and telemetry."""
    def __init__(self):
        self.state = ESP32State.BOOTING
        self.start_time = time.time()
        self.battery_level = 85.0
        self.is_charging = False
        self.wifi_connected = False
        self.ip_address = "0.0.0.0"
        self.free_heap = 320000 # Simulated 320KB
        self.last_error = ""
        self.uptime = 0

    def update(self):
        self.uptime = int(time.time() - self.start_time)
        
        # Simple battery drain simulation
        if not self.is_charging and self.battery_level > 0:
            self.battery_level -= 0.001
            
        if self.battery_level < 5:
            self.state = ESP32State.LOW_BATTERY

    def set_state(self, new_state: ESP32State):
        self.state = new_state

    def connect_wifi(self):
        self.wifi_connected = True
        self.ip_address = "192.168.1.42"
