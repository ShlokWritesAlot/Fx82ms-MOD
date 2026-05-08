from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import Qt
from ui.styles import OLED_STYLE, OLED_LABEL_STYLE

class OLEDView(QWidget):
    """Simulates a 0.91 inch 128x32 OLED module."""
    def __init__(self):
        super().__init__()
        # Optimized OLED module height to prevent clipping (160x60)
        self.setFixedSize(160, 60) 
        self.setStyleSheet(OLED_STYLE)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.display.setFrameStyle(0)
        self.display.setStyleSheet(OLED_LABEL_STYLE)
        self.display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Force zero internal margins to prevent clipping
        self.display.document().setDocumentMargin(0)
        
        layout.addWidget(self.display)
        self.setLayout(layout)

    def update_display(self, lines):
        """Updates the text with proper spacing."""
        text = "\n".join(lines)
        self.display.setPlainText(text)

    def clear(self):
        self.display.clear()
