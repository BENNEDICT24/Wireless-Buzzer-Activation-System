import socket # Import the socket module to use networking features

host = "172.21.12.32" # IP address of the server
port = 12345 # Port number the server is listening on
buffer_size = 1024 # Size of buffer to receive server response

# Create a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(0.1)

while True:
    # Prompt user for input and standardize the command format
    command = input("Enter command (ACTIVATE/DEACTIVATE or EXIT to quit): ").strip().upper()
    
    # Handle the EXIT command
    if command == "EXIT":
        print("Exiting client...")
        message="EXIT"  # Message to send to server to indicate termination
    
    # Handle the ACTIVATE command
    elif command == "ACTIVATE":
        print("Sending command: ACTIVATE")
        message = "ACTIVATE" # Command to activate the server-side process
    
    # Handle the DEACTIVATE command
    elif command == "DEACTIVATE":
        print("Sending command: DEACTIVATE")
        message = "DEACTIVATE" # Command to deactivate the server-side process
    
    # If the command is not valid, prompt again
    else:
        print("Invalid command... Please enter 'ACTIVATE' or 'DEACTIVATE'.")
        continue # Skip the rest and go back to the start of the loop

    try:
        # Send the command to the server
        client.sendto(message.encode(), (host, port))
        # Wait for a response from the server
        response, _ = client.recvfrom(buffer_size)
        print(f"Receiving  response: {response.decode()}")
    
    # Handle timeout if the server does not respond in time
    except socket.timeout:
        print("The connection timed out")
    
    # Catch any other exceptions that may occur
    except Exception as e:  
        print(f"An error occurred: {e}")
# Close the client socket when exiting the loop
print("Closing the connection...")
client.close() 