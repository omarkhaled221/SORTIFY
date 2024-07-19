from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import RPi.GPIO as GPIO
import time

# Initialize LCD and GPIO
lcd = LCD()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Disable GPIO warnings

# Keypad layout (4x4 matrix)
rows = [16, 20, 21, 5]    # GPIO pins for rows R1, R2, R3, R4
cols = [6, 13, 19, 26]     # GPIO pins for columns C1, C2, C3, C4
keypad_map = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Set up GPIO for keypad
for row in rows:
    GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for col in cols:
    GPIO.setup(col, GPIO.OUT)

# Function to read keypad input
def read_keypad():
    for col_num, col_pin in enumerate(cols):
        GPIO.output(col_pin, GPIO.HIGH)  # Activate column
        for row_num, row_pin in enumerate(rows):
            if GPIO.input(row_pin) == GPIO.HIGH:
                time.sleep(0.1)  # Add a small delay to debounce and stabilize input
                return keypad_map[row_num][col_num]
        GPIO.output(col_pin, GPIO.LOW)  # Deactivate column
    return None  # No key pressed

# Function for safe exit
def safe_exit(signum, frame):
    lcd.clear()
    GPIO.cleanup()
    exit(1)

# Set up signal handlers for termination signals
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

# Display "Welcome to SORTIFY" for 3 seconds
lcd.text("Welcome to", 1)
lcd.text("SORTIFY", 2)
time.sleep(3)
lcd.clear()

phone_number = ""

try:
    lcd.text("Press button A", 1)
    while True:
        key = read_keypad()
        if key == 'A':
            lcd.clear()
            lcd.text("Enter number", 1)
            lcd.text("", 2)  # Clear previous phone number display
            break
        time.sleep(0.2)  # Adjust delay as needed for responsiveness

    while True:
        key = read_keypad()
        if key is not None:
            if key.isdigit():
                phone_number += key
                lcd.text(phone_number, 2)
            elif key == 'B':
                lcd.clear()
                lcd.text("Phone number saved", 1)
                lcd.text(phone_number, 2)
                break
            elif key == 'D':
                phone_number = ""  # Clear entered number if 'D' is pressed
                lcd.clear()
                lcd.text("Enter number", 1)
                lcd.text("", 2)
        time.sleep(0.2)  # Adjust delay to prevent rapid key repeat

except KeyboardInterrupt:
    lcd.clear()
    GPIO.cleanup()