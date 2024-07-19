from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
cred = credentials.Certificate("/home/pi/Desktop/sortify-sydw2v-firebase-adminsdk-7t5yi-38686b33ef.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize LCD and GPIO
lcd = LCD()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Keypad layout (4x4 matrix)
rows = [16, 20, 21, 5]  # GPIO pins for rows R1, R2, R3, R4
cols = [6, 13, 19, 26]  # GPIO pins for columns C1, C2, C3, C4
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
        GPIO.output(col_pin, GPIO.HIGH)
        for row_num, row_pin in enumerate(rows):
            if GPIO.input(row_pin) == GPIO.HIGH:
                time.sleep(0.1)
                return keypad_map[row_num][col_num]
        GPIO.output(col_pin, GPIO.LOW)
    return None

# Function for safe exit
def safe_exit(signum, frame):
    lcd.clear()
    GPIO.cleanup()
    exit(1)

# Set up signal handlers
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

lcd.text("Welcome to", 1)
lcd.text("SORTIFY", 2)
time.sleep(3)
lcd.clear()

phone_number = ""

try:
    lcd.text("Enter number", 1)
    while True:
        key = read_keypad()
        if key and key.isdigit():
            phone_number += key
            lcd.text(phone_number, 2)
        elif key == 'B':
            break
        elif key == 'D':
            phone_number = ""
            lcd.clear()
            lcd.text("Enter number", 1)
        time.sleep(0.2)

    lcd.clear()
    lcd.text("Checking...", 1)

    user_ref = db.collection('user').where('phone_number', '==', phone_number).limit(1).get()

    if user_ref:
        user_data = user_ref[0]
        current_points = int(user_data.get('total_points') or 0)

        lcd.clear()
        lcd.text("Enter items no.", 1)
        entered_items = ""
        while True:
            key = read_keypad()
            if key and key.isdigit() and int(key) in range(1, 10):
                entered_items += key
                lcd.text(entered_items, 2)
            elif key == 'B':
                entered_items = int(entered_items) if entered_items else 0
                new_points = current_points + entered_items
                user_ref[0].reference.update({'total_points': new_points})
                lcd.clear()
                lcd.text("Items saved!", 1)
                break
            elif key == 'D':
                entered_items = ""
                lcd.clear()
                lcd.text("Enter items no.", 1)
            time.sleep(0.2)
    else:
        lcd.clear()
        lcd.text("Incorrect Number", 1)
        time.sleep(3)

except KeyboardInterrupt:
    pass
finally:
    lcd.clear()
    GPIO.cleanup()