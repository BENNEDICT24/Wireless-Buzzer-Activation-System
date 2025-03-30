import RPi.GPIO as GPIO 
import socket
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Button GPIO pin
btn_pin = 17    #he button will be connected to GPIO 17 on the Raspberry Pi.
# Buzzer GPIO pin
buzzer_pin = 18  #the passive buzzer will be connected to GPIO 18.

# Set up the button and buzzer pins
GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)

# UDP configuration
IP_addr = "255.255.255.255"  # Broadcast IP to reach all devices in the networ
PORT= 5005  # Port to send messages to
MESSAGE = "EMERGENCY!"  # The message to send

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Function that will be used to send the message 
def send_alert():
    sock.sendto(MESSAGE.encode(), (IP_addr, PORT))
    print("Alert sent to all clients!")

# Main loop to monitor the button press
try:
    last_button_state = GPIO.HIGH  # Button is not pressed by default (active-high)
    while True:
        input_state = GPIO.input(btn_pin)
        if input_state == GPIO.LOW and last_button_state == GPIO.HIGH:  # If the button is pressed that is when the GPIO is low, te it will enter the if statement 
            print("Button pressed!")
            # Sound the buzzer
            GPIO.output(buzzer_pin, GPIO.HIGH)
            # Send the emergency message to clients
            send_alert()
            time.sleep(2)  # Debounce delay
            GPIO.output(buzzer_pin, GPIO.LOW)
        time.sleep(0.1)  # Small delay to avoid 100% CPU usage

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
    sock.close()  # Close the socket