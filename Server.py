import socket
import RPi.GPIO as GPIO

# Constants for buzzer pin and PWM frequency
BUZZER_PIN = 23
FREQ = 1000

# GPIO setup for buzzer
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
pwm = GPIO.PWM(BUZZER_PIN, FREQ)
pwm_started = False  # Flag to track buzzer state

def handle_pwm_command(command):
    """
    Processes commands to activate, deactivate, or stop the server.
    """
    global pwm_started
    command = command.strip().lower()  # Clean and normalize the command

    if command == "activate":
        if not pwm_started:
            pwm.start(50)  # Start PWM with 50% duty cycle
            pwm_started = True
            return "Buzzer activated"
        else:
            return "Buzzer is already activated"
        
    elif command == "deactivate":
        if pwm_started:
            pwm.stop()  # Stop the buzzer
            pwm_started = False
            return "Buzzer deactivated"
        else:
            return "Buzzer is already deactivated"
        
    elif command == "exit":
        if pwm_started:
            pwm.stop()  # Ensure buzzer is off before exiting
        GPIO.cleanup()  # Clean up GPIO settings
        return "Server is exiting"
    
    else:
        return "Unknown Command"  # Handle invalid commands

def run_pwm_server(host="172.21.12.32", port=12345):
    """
    Starts a UDP server that listens for commands to control the buzzer.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))  # Bind the server to a specific IP and port
        print(f"Buzzer server listening on {host}:{port}")
        
        while True:
            data, addr = s.recvfrom(1024)  # Receive data from client
            command = data.decode()  # Decode the command
            response = handle_pwm_command(command)  # Process the command
            s.sendto(response.encode(), addr)  # Send back the response
            
            if command.strip().lower() == "exit":
                break  # Exit the server if the "exit" command is received

if __name__ == "__main__":
    """
    Main function that starts the server and handles cleanup on interrupt.
    """
    try:
        run_pwm_server()  # Start the server
    except KeyboardInterrupt:
        if pwm_started:
            pwm.stop()  # Stop PWM if it was running
        GPIO.cleanup()  # Clean up GPIO settings on exit
        print("Interrupted. GPIO cleaned up.")