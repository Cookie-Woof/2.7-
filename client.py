"""
Client Program

Connects to the server and sends commands with byte-count verification.

Protocol: Send length (4 bytes) + data
Example: "0015" + "dir C:\Users" (15 bytes)

Author: Ariel Melamed Cohen
Grade: 11th Grade, 3rd Class
Date: 14/11/2025
"""

import socket
import logging

IP = "192.168.50.104"
PORT = 6000

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MAX_PACKET = 4096


def send_message(client_socket, message):
    """
    Sends a message to the server with byte count.
    
    We count how many bytes we're sending, put that number first (4 bytes),
    then send the actual message. The server will verify it got the right amount.
    """
    # Convert message to bytes and count them
    message_bytes = message.encode()
    message_length = len(message_bytes)
    
    # Create the length prefix (4 digits, like "0015")
    length_counter = f"{message_length:04d}".encode()
    
    # Send length + message
    client_socket.send(length_counter + message_bytes)
    logging.info(f"Sent {message_length} bytes: {message}")


def receive_message(client_socket):
    """
    Receives a message from the server using the protocol.
    
    First we get 4 bytes telling us how much data is coming,
    then we receive that exact amount and verify we got it all.
    """
    # Step 1: Receive the first 4 bytes (the length) - PROPERLY
    length_data = b""
    while len(length_data) < 4:
        chunk = client_socket.recv(4 - len(length_data))
        if not chunk:
            return None
        length_data += chunk
    
    expected_length = int(length_data.decode())
    logging.info(f"Server says they're sending {expected_length} bytes")
    
    # Step 2: Receive the actual data
    data = b""
    bytes_received = 0
    
    while bytes_received < expected_length:
        chunk = client_socket.recv(min(expected_length - bytes_received, MAX_PACKET))
        if not chunk:
            break
        data += chunk
        bytes_received += len(chunk)
    
    # Step 3: Check if we got what we expected
    actual_length = len(data)
    
    if actual_length == expected_length:
        logging.info(f"✓ Verified: received {actual_length} bytes (matches expected)")
        return data.decode()
    else:
        logging.warning(f"✗ Mismatch: expected {expected_length} bytes but got {actual_length}")
        return None


def main():
    """
    Main client function.
    
    Connects to the server and lets you type commands.
    Uses our protocol to send/receive with byte count verification.
    """
    # Create client socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    assert my_socket, "Failed to create socket"

    try:
        # Connect to server
        my_socket.connect((IP, PORT))
        logging.info("Connected to server with byte-count protocol")
       
        try:
            while True:
                msg = input("Enter command: ")
                assert isinstance(msg, str), "Input must be a string"
                
                send_message(my_socket, msg)
               
                response = receive_message(my_socket)
                
                if not response:
                    logging.error("No response received or protocol error")
                    break
               
                assert isinstance(response, str), "Response must be a string"
               
                print("Server:", response)
                   
                if msg.lower() == "exit":
                    assert msg.lower() == "exit", "Exit command verification failed"
                    logging.info("Exiting client")
                    break   
                    
        except Exception as e:
            logging.error(f"Couldn't input/receive: {e}")
           
    except socket.error as err:
        logging.error(f'Received socket error: {err}')

    finally:
        my_socket.close()
        logging.info("Connection closed")


if __name__ == "__main__":
    main()