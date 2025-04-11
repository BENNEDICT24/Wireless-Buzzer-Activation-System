import socket
import RPi.GPIO as GPIO

BUZZER_PIN = 23
FREQ = 1000

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
pwm = GPIO.PWM(BUZZER_PIN, FREQ)
pwm_started = False

def handle_pwm_command(command):
    global pwm_started
    command = command.strip().lower()
    
    if command == "activate":
        if not pwm_started:
            pwm.start(50)
            pwm_started = True
            print("Buzzer activated")
            return "Buzzer activated"
        else:
            return "Buzzer is already activated"
        
    elif command == "deactivate":
        if pwm_started:
            pwm.stop()
            pwm_started = False
            print("Buzzer deactivated")
            return "Buzzer deactivated"
        else:
            return "Buzzer is already deactivated"
        
    elif command == "exit":
            if pwm_started:
                pwm.stop()
            GPIO.cleanup()
            print("Server is exiting")
            return "Server is exiting"
            
    else:
            return "Unknown Command"
        
def run_pwm_server(host="172.21.12.32", port=12345):
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.bind((host,port))
        print(f"Buzzer server listening on {host}:{port}")
        
        while True:
            data, addr = s.recvfrom(1024)
            command = data.decode()
            response = handle_pwm_command(command)
            s.sendto(response.encode(), addr)
            
            if command.strip().lower() == "exit":
                break
                
if __name__=="__main__":
    try:
        run_pwm_server()
    except KeyboardInterrupt:
        if pwm_started:
            pwm.stop()
        GPIO.cleanup()
        print("Interrupted. GPIO cleaned up.")
