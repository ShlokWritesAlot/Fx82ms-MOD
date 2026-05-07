from ..config import settings

class StatusBar:
    """Simulates the top status bar (WiFi, Battery)."""
    
    @staticmethod
    def get_status_line():
        wifi = "W:" + "|" * settings.WIFI_STRENGTH
        batt = "B:" + str(settings.BATTERY_LEVEL) + "%"
        # Combine and pad
        space = settings.SCREEN_COLS - len(wifi) - len(batt)
        return wifi + (" " * space) + batt
