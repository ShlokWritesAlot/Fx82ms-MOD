import json
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QVBoxLayout, QFrame, QHBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt

class CalculatorView(QWidget):
    """Visual representation of the fx-82MS keypad with sub-labels."""
    key_pressed = Signal(dict)

    def __init__(self, keymap_path):
        super().__init__()
        self.load_keymap(keymap_path)
        self.init_ui()

    def load_keymap(self, path):
        with open(path, 'r') as f:
            self.keymap = json.load(f)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Grid for buttons
        grid = QGridLayout()
        grid.setSpacing(4)
        grid.setContentsMargins(5, 5, 5, 5)
        
        for key_info in self.keymap['keys']:
            container = QWidget()
            cont_layout = QVBoxLayout(container)
            cont_layout.setContentsMargins(0, 0, 0, 0)
            cont_layout.setSpacing(2)
            
            # Sub-label (ABC, DEF, etc.)
            sub_text = key_info.get('sublabel', "")
            sub_lbl = QLabel(sub_text)
            sub_lbl.setAlignment(Qt.AlignCenter)
            sub_lbl.setStyleSheet("color: #e0e0e0; font-size: 8px; font-weight: bold; font-family: Arial;")
            if not sub_text:
                sub_lbl.setStyleSheet("color: transparent;")
            
            cont_layout.addWidget(sub_lbl)
            
            # Main Button
            btn = QPushButton(key_info['label'])
            size = key_info.get('size', [42, 26])
            btn.setFixedSize(size[0], size[1])
            
            bg_color = key_info.get('color', '#212121')
            text_color = key_info.get('text_color', '#fff')
            
            # Premium 3D Styling
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 {bg_color}, stop:1 #1a1a1a);
                    color: {text_color};
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 9px;
                    border-bottom: 2px solid #000;
                    border-right: 1px solid #000;
                }}
                QPushButton:pressed {{
                    background-color: #000;
                    border-bottom: 1px solid #000;
                    margin-top: 2px;
                }}
            """)
            
            btn.pressed.connect(lambda k=key_info: self.key_pressed.emit(k))
            cont_layout.addWidget(btn)
            
            grid.addWidget(container, key_info['row'], key_info['col'])

        layout.addLayout(grid)
        self.setLayout(layout)
