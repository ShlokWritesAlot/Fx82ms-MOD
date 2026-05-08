import os

# Display settings (Simulating 128x32 OLED)
OLED_WIDTH = 128
OLED_HEIGHT = 32
SCREEN_ROWS = 4
SCREEN_COLS = 21  # Approx characters per line for 128px wide with small font

# Colors (Simulating monochrome OLED)
COLOR_BG = 0
COLOR_FG = 1

# API settings
API_BASE_URL = "http://localhost:8001"
ASK_ENDPOINT = "/ask"
TIMEOUT_SECONDS = 30

# UI Settings
BATTERY_LEVEL = 85
WIFI_STRENGTH = 3
DEVICE_NAME = "CASIO fx-82MS"
VERSION = "v1.0.4-AI"
