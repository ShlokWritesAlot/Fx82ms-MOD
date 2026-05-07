from abc import ABC, abstractmethod

class BaseScreen(ABC):
    """Base class for all UI screens."""
    
    def __init__(self, renderer):
        self.renderer = renderer
        self.is_active = True

    @abstractmethod
    def update(self):
        """Update screen logic."""
        pass

    @abstractmethod
    def render(self):
        """Draw to the renderer buffer."""
        pass

    @abstractmethod
    def handle_input(self, event):
        """Handle input events."""
        pass
