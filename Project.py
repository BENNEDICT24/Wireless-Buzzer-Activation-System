import RPi.GPIO as GPIO
import socket
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Button GPIO pin
btn_pin = 17  # The button will be connected to GPIO 17 on the Raspberry Pi.
# Buzzer GPIO pin
buzzer_pin = 18  # The passive buzzer will be connected to GPIO 18.

# Set up the button and buzzer pins
GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)

# UDP configuration
IP_addr = "255.255.255.255"  # Broadcast IP to reach all devices in the network
PORT = 5005  # Port to send messages to
MESSAGE = "EMERGENCY!"  # The message to send
ACTIVATE_MSG = "ACTIVATE"
DEACTIVATE_MSG = "DEACTIVATE"

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Function that will be used to send the emergency message
def send_alert():
    sock.sendto(MESSAGE.encode(), (IP_addr, PORT))
    print("Alert sent to all clients!")

# Function to handle the buzzer control
def control_buzzer(state):
    if state == "ACTIVATE":
        GPIO.output(buzzer_pin, GPIO.HIGH)  # Activate buzzer
        print("Buzzer activated.")
    elif state == "DEACTIVATE":
        GPIO.output(buzzer_pin, GPIO.LOW)  # Deactivate buzzer
        print("Buzzer deactivated.")
    else:
        print("Unknown command received.")

# Server to listen for UDP messages (ACTIVATE/DEACTIVATE)
def listen_for_commands():
    sock.bind(('', PORT))  # Listen on the specified port
    while True:
        try:
            data, addr = sock.recvfrom(1024)  # Receive message from client
            message = data.decode()

            # Acknowledge the command and control buzzer accordingly
            if message == ACTIVATE_MSG:
                control_buzzer("ACTIVATE")
                sock.sendto("Buzzer activated.".encode(), addr)  # Acknowledge
            elif message == DEACTIVATE_MSG:
                control_buzzer("DEACTIVATE")
                sock.sendto("Buzzer deactivated.".encode(), addr)  # Acknowledge
            else:
                sock.sendto("Unknown command.".encode(), addr)  # Acknowledge invalid commands

        except KeyboardInterrupt:
            print("Server interrupted.")
            break

# Main loop to monitor the button press and send alerts
try:
    last_button_state = GPIO.HIGH  # Button is not pressed by default (active-high)
    while True:
        input_state = GPIO.input(btn_pin)
        if input_state == GPIO.LOW and last_button_state == GPIO.HIGH:  # If the button is pressed (GPIO is low)
            print("Button pressed!")
            # Send the emergency message to clients
            send_alert()
            time.sleep(2)  # Debounce delay
        last_button_state = input_state  # Update the button state
        time.sleep(0.1)  # Small delay to avoid 100% CPU usage

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
    sock.close()  # Close the socket

# Run the server function in a separate thread or process to allow both server listening and button press handling simultaneously