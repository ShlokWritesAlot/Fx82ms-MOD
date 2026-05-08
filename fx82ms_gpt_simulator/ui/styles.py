DARK_THEME = """
QMainWindow {
    background-color: #121212;
}

QGroupBox {
    color: #e0e0e0;
    border: 1px solid #333;
    margin-top: 15px;
    font-weight: bold;
    border-radius: 5px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    left: 10px;
}

QLabel {
    color: #e0e0e0;
}

QPushButton {
    background-color: #333;
    color: white;
    border-radius: 5px;
    padding: 5px;
}

QPushButton:pressed {
    background-color: #555;
}

QTextEdit {
    background-color: #1e1e1e;
    color: #00ff00;
    font-family: 'Consolas', monospace;
    border: 1px solid #333;
}
"""

OLED_STYLE = """
    QWidget {
        background-color: #000000;
        border: 4px solid #1a1a1a;
        border-radius: 2px;
    }
    #oled_frame {
        background-color: #000;
        border: 1px solid #333;
        padding: 5px;
    }
"""

OLED_LABEL_STYLE = """
    QTextEdit {
        color: #00d4ff;
        font-family: 'Courier New', monospace;
        font-size: 10px;
        font-weight: bold;
        line-height: 100%;
        background: transparent;
        border: none;
        padding: 0px;
        margin: 0px;
    }
"""

DARK_THEME += """
#calc_shell {
    background-color: #37474f;
    border: 3px solid #263238;
}
"""
