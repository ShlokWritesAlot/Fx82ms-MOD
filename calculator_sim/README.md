# Casio FX-82MS GPT Simulator

This is a terminal-based simulator for the Casio FX-82MS AI Mod. It emulates the 128x32 OLED display and keypad navigation of the final hardware.

## Features
- **OLED Emulation**: 128x32 resolution simulation (4 text lines).
- **Keypad Controls**: Mapped to keyboard (W/S/A/D/ENTER/ESC).
- **AI Integration**: Connects to the local FastAPI bridge and Ollama.
- **Embedded UX**: Low-screen-space optimized menus and response formatting.
- **Modular Design**: Clean separation between rendering, input, and logic.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: On Windows, this installs `windows-curses` for terminal UI.*

2. **Start the API Bridge**:
   Ensure your FastAPI bridge and Ollama are running:
   ```bash
   python ../main.py
   ```

3. **Run the Simulator**:
   ```bash
   python run_sim.py
   ```

## Controls
- **W / S**: Navigate Up/Down
- **ENTER**: Select / Send Prompt
- **ESC / Q**: Back to Menu
- **BACKSPACE**: Delete character
- **A-Z / 0-9**: Type prompt in "Ask AI" mode
- **SPACE**: Page through long AI responses

## Architecture Explanation

### 1. Rendering Layer (`rendering/oled.py`)
Simulates the SSD1306 OLED buffer. Instead of drawing pixels, it manages a 4-line text buffer that mimics the character density of the real display.

### 2. Input Layer (`input/handler.py`)
Decouples physical key codes from logic events. In the final hardware, this file would be replaced with a GPIO-based scanner for the MCP23017.

### 3. API Client (`api/client.py`)
Handles asynchronous requests to the local bridge. Implements timeouts and error handling to simulate network latency on the ESP32.

### 4. Text Engine (`utils/text_engine.py`)
Crucial for the tiny display. Handles word wrapping and pagination so that a long AI response can be read 4 lines at a time.

### 5. Screen System (`screens/`)
Each UI mode (Menu, Ask AI, Splash) is a self-contained class inheriting from `BaseScreen`. This makes it easy to add new calculator functions.

## Mapping to Hardware
- **ESP32**: The `app.py` loop and screen logic will port directly to MicroPython/C++ on the ESP32.
- **MCP23017**: The `InputHandler` will eventually read from the I2C registers of the MCP23017 instead of `curses.getch()`.
- **SSD1306**: The `OLEDRenderer` will write to the I2C display buffer instead of a terminal window.
