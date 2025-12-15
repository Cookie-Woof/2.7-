# Client Program

# Connects to the server and sends commands with byte-count verification.

# Protocol: Send length (4 bytes) + data
# Example: "0015" + "dir C:\Users" (15 bytes)

# Author: Ariel Melamed Cohen
# Grade: 11th Grade, 3rd Class
# Date: 14/11/2025


import socket
import logging

IP = "192.168.50.104"
PORT = 6000

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MAX_PACKET = 4096


def send_message(client_socket, message):
    """
    Sends a message to the server with byte count.

    We count how many bytes we're sending, put that number first (4 bytes),
    then send the actual message. The server will verify it got the right
    amount.
    """
    assert isinstance(message, str), "Message must be a string"
    assert len(message) > 0, "Message cannot be empty"
    
    # Convert message to bytes and count them
    message_bytes = message.encode()
    message_length = len(message_bytes)
    assert message_length < 10000, "Message too large (max 9999 bytes)"

    # Create the length prefix (4 digits, like "0015")
    length_counter = f"{message_length:04d}".encode()
    assert len(length_counter) == 4, "Length prefix must be exactly 4 bytes"

    # Send length + message
    client_socket.send(length_counter + message_bytes)
    logging.info(f"Sent {message_length} bytes: {message}")


def receive_message(client_socket):
    """
    Receives a message from the server using the protocol.

    First we get 4 bytes telling us how much data is coming,
    then we receive that exact amount and verify we got it all.
    """
    length_data = b""
    while len(length_data) < 4:
        chunk = client_socket.recv(4 - len(length_data))
        if not chunk:
            return None
        length_data += chunk

    assert len(length_data) == 4, "Length prefix must be 4 bytes"
    expected_length = int(length_data.decode())
    assert expected_length >= 0, "Expected length cannot be negative"
    logging.info(f"Server says they're sending {expected_length} bytes")

    data = b""
    bytes_received = 0

    while bytes_received < expected_length:
        chunk = client_socket.recv(
            min(expected_length - bytes_received, MAX_PACKET)
        )
        if not chunk:
            break
        data += chunk
        bytes_received += len(chunk)

    actual_length = len(data)

    if actual_length == expected_length:
        logging.info(
            f"Verified: received {actual_length} bytes (matches expected)"
        )
        return data.decode()
    else:
        logging.warning(
            f"Erorr: expected {expected_length} bytes "
            f"but got {actual_length}"
        )
        return None


def main():
    """
    Main client function.

    Connects to the server and lets you type commands.
    Uses our protocol to send/receive with byte count verification.
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    assert my_socket, "Failed to create socket"
    assert PORT > 0 and PORT < 65536, "Invalid port number"

    try:
        my_socket.connect((IP, PORT))
        logging.info("Connected to server with byte-count protocol")

        try:
            print(          "Commands you can use: \n", 
            "  DIR <path> - See what files are in a folder \n",
            "  DELETE <path> - Remove a file \n",
            "  COPY <source>,<dest> - Copy a file \n",
            "  EXECUTE <path> - Run a program \n",
            "  TAKE SCREENSHOT - Take a picture of the screen \n",
            "  SAVE SCREENSHOT <path> - Save the screenshot \n",
            "  HELP - Show this message \n",
            "  EXIT - Disconnect \n")

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