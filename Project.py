import RPi.GPIO as GPIO
import socket

# Configure the GPIO for the buzzer
BUZZER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Server settings
SERVER_IP = '0.0.0.0'  # Listen on all available interfaces
SERVER_PORT = 12345     # Port to listen on

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))  # Bind the server to the specified IP and port

print("Server listening on port", SERVER_PORT)

def control_buzzer(command):
    """Control the buzzer based on the command received."""
    if command == 'ACTIVATE':
        GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Activate the buzzer
        print("Buzzer activated")
        return "Buzzer Activated"
    elif command == 'DEACTIVATE':
        GPIO.output(BUZZER_PIN, GPIO.LOW)   # Deactivate the buzzer
        print("Buzzer deactivated")
        return "Buzzer Deactivated"
    else:
        print("Invalid command")
        return "Invalid command"

try:
    while True:
        # The server listens for incoming UDP packets using recvfrom.
        data, client_address = server_socket.recvfrom(1024)  # 'recvfrom' is the listening method
        command = data.decode('utf-8')

        print(f"Received command: {command} from {client_address}")
        
        # Control the buzzer based on the command received and get a response
        response = control_buzzer(command)

        # Send a response back to the client
        server_socket.sendto(response.encode('utf-8'), client_address)

except KeyboardInterrupt:
    print("Server shutting down...")
finally:
    GPIO.cleanup()
    server_socket.close()