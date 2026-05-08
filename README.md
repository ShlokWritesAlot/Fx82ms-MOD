# Casio fx-82MS GPT Desktop Simulator

You can now simulate this project at wowki at **https://wokwi.com/projects/463440511518280705**

This is a professional desktop GUI simulator for the Casio fx-82MS AI Mod project. It allows you to test the full system behavior—from matrix scanning to AI response formatting—before your hardware arrives.

## Features
- **Visual Keypad**: Interactive grid of calculator buttons.
- **OLED Simulation**: 128x32 blue monochrome display with 4-line text rendering.
- **Hardware Simulation**:
  - **ESP32-C3**: State machine, WiFi, battery, and telemetry.
  - **MCP23017**: 8x8 matrix scanning simulation with active row tracking.
- **AI Backend**: Connects to the local FastAPI bridge and Ollama.
- **Debug Panel**: Real-time telemetry, matrix bitmasks, and API logs.
- **Smart Formatting**: Word wrapping and pagination for tiny displays.

## Setup

1. **Install Requirements**:
   ```bash
   pip install PySide6 httpx pydantic
   ```

2. **Run the Simulator**:
   ```bash
   python main.py
   ```

## Keypad Mode
- **GPT / ASK**: Enter AI input mode.
- **Numbers/Operators**: Type your prompt.
- **SEND**: Submit to AI.
- **MORE**: Cycle through pages of long responses.
- **BACK**: Return to main menu.
- **DEL / AC**: Delete or Clear input.

## How it Maps to Hardware
- **ESP32 Firmware**: The states in `esp32_sim.py` and the logic in `main_window.py` map directly to your main loop in C++/MicroPython.
- **MCP23017**: The `scan()` method in `mcp23017_sim.py` simulates the exact logic you'll use to pull rows low and read column states.
- **SSD1306**: the `update_display()` calls in `oled_view.py` will be replaced by `display.println()` or buffer writes to the I2C OLED.
