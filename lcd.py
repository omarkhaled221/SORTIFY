from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import atexit

# Initialize the LCD
lcd = LCD()

def safe_exit(signum, frame):
    lcd.clear()
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

try:
    lcd.text("Welcome to ", 1)
    lcd.text("Sortify ", 2)
    pause()

except KeyboardInterrupt:
    pass

finally:
    lcd.clear()