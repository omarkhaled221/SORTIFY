import RPi.GPIO as GPIO
import time

# Define the GPIO pins for the rows and columns
ROWS = [17, 27, 22, 5]
COLS = [23, 24, 25, 16]

# Define the keys in the keypad
KEYPAD = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

def setup():
    GPIO.setmode(GPIO.BCM)
    # Setup rows as outputs and set them to high
    for row in ROWS:
        GPIO.setup(row, GPIO.OUT)
        GPIO.output(row, GPIO.HIGH)
    # Setup columns as inputs with pull-up resistors
    for col in COLS:
        GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_key():
    # Scan rows to find the pressed key
    for row in ROWS:
        GPIO.output(row, GPIO.LOW)
        for col in COLS:
            if GPIO.input(col) == GPIO.LOW:
                # Wait for the key to be released
                while GPIO.input(col) == GPIO.LOW:
                    time.sleep(0.1)
                GPIO.output(row, GPIO.HIGH)
                return KEYPAD[ROWS.index(row)][COLS.index(col)]
        GPIO.output(row, GPIO.HIGH)
    return None

def main():
    setup()
    print("Press keys on the keypad:")
    try:
        while True:
            key = get_key()
            if key:
                print("Key pressed:", key)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nProgram exited")
    finally:
        GPIO.cleanup()

if _name_ == "_main_":
    main()