
# Client and Server Program - SERVER SIDE

# This server lets you remotely manage files on a computer.

# Commands you can use:
#     - DIR: See what files are in a folder
#     - DELETE: Remove a file
#     - COPY: Copy the info from one file to another
#     - EXECUTE: Run a program
#     - TAKE SCREENSHOT: Take a picture of the screen
#     - SAVE SCREENSHOT: Save the screenshot you took
#     - EXIT: Disconnect

# Author: Ariel Melamed Cohen
# Grade: 11th Grade, 3rd Class
# Date: 14/11/2025


import socket
import logging
import os
import glob
import shutil
import subprocess
import pyautogui


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

QUEUE_LEN = 1
MAX_PACKET = 1024
last_screenshot = None


def check_for_path(path):
    """
    Checks if a file or folder exists on the computer.
    We use this before trying to do anything with files to make sure
    they actually exist.
    """
    assert isinstance(path, str), "Path must be a string"
    return os.path.exists(path)


def save_screenshot(path):
    """
    Saves the last screenshot that the program had took to a file.
    The path is where you want to save the image.
    """
    global last_screenshot
    assert isinstance(path, str), "Path must be a string"
    
    try:
        if last_screenshot is None:
            return ("Error: No screenshot to save. "
                    "Please use 'take screenshot' first!")

        last_screenshot.save(path)
        return f"Screenshot saved to: {path}"
    except Exception as e:
        logging.error(f"Problem saving screenshot: {e}")
        return f"Error saving screenshot: {e}"


def take_screenshot():
    """
    Takes a screenshot of the entire screen and stores it in the program's
    memory. You need to use 'save screenshot' afterwards to actually save
    it to a file.
    """
    global last_screenshot
    try:
        last_screenshot = pyautogui.screenshot()
        assert last_screenshot is not None, "Screenshot capture failed"
        return "Screenshot captured! Use 'save screenshot <path>' to save it."

    except Exception as e:
        logging.error(f"Problem taking screenshot: {e}")
        return f"Error couldn't take a screenshot: {e}"


def dir_command(path):
    """
    Lists all the files in a folder.
    Give it a path like "C:\\Users" and it'll show you everything inside.
    If the folder is empty, it'll let you know.
    """
    assert isinstance(path, str), "Path must be a string"
    
    try:
        files_list = glob.glob(path + '\\*')

        if files_list:
            result = "Files found:\n" + "\n".join(files_list)
        else:
            result = f"No files found in {path}"

        return result
    except Exception as e:
        logging.error(f"Problem with dir command: {e}")
        return f"Error with dir command: {e}"


def delete_command(path):
    """
    Deletes a file from the computer.
    Just give it the full path to the file and it's gone to the trash.
    """
    assert isinstance(path, str), "Path must be a string"
    assert os.path.exists(path), f"File does not exist: {path}"
    
    try:
        os.remove(path)
        return f"File removed successfully! {path}"
    except Exception as e:
        logging.error(f"The file {path} couldn't be removed: {e}")
        return f"Error: Couldn't delete file: {e}"


def copy_file_command(source_path, dest_path):
    """
    Copies a file from one location to another.
    Takes the content from source_path and puts it in dest_path.
    If dest_path doesn't exist, it creates it. If it does exist, it
    overwrites it.
    """
    assert isinstance(source_path, str), "Source path must be a string"
    assert isinstance(dest_path, str), "Destination path must be a string"
    assert os.path.exists(source_path), f"Source file not found: {source_path}"
    
    try:
        shutil.copy(source_path, dest_path)
        return f"File copied successfully from {source_path} to {dest_path}"
    except Exception as e:
        logging.error(f"Couldn't copy the file: {e}")
        return f"Error: Couldn't copy file: {e}"


def excute_command(path):
    """
    Runs the program which is in <path> it can run codes and
    even built in programs.
    """
    assert isinstance(path, str), "Path must be a string"
    
    try:
        subprocess.Popen([path])
        return f"Executing: {path}"
    except Exception as e:
        logging.error(f"Couldn't execute file: {e}")
        return f"Error: Couldn't execute file: {e}"


def handle_command(command):
    """
    This is the brain of the server - it figures out what command the client
    sent and calls the right function to handle it.

    It checks if paths exist before doing anything dangerous, and returns
    helpful error messages if something goes wrong.

    Commands it understands:
        - "dir C:\\path" - list files
        - "delete C:\\file.txt" - delete a file
        - "copy C:\\source.txt,C:\\dest.txt" - copy (notice the comma!)
        - "excute C:\\program.exe" - run a program
        - "save screenshot C:\\pic.jpg" - save screenshot
        - "exit" - disconnect
    """
    assert isinstance(command, str), "Command must be a string"
    command = command.strip().lower()

    if command.startswith("dir "):
        path = command[4:].strip()
        check_for_path(path)
        return dir_command(path)

    elif command == "take screenshot":
        return take_screenshot()

    elif command.startswith("save screenshot "):
        path = command[16:].strip()
        return save_screenshot(path)

    elif command.startswith("delete "):
        path = command[7:].strip()
        check_for_path(path)
        return delete_command(path)

    elif command.startswith("excute "):
        path = command[7:].strip()
        check_for_path(path)
        return excute_command(path)
    
    elif command == "help":
        help_text = [
            "Commands you can use:",
            "  DIR <path> - See what files are in a folder",
            "  DELETE <path> - Remove a file",
            "  COPY <source>,<dest> - Copy a file",
            "  EXECUTE <path> - Run a program",
            "  TAKE SCREENSHOT - Take a picture of the screen",
            "  SAVE SCREENSHOT <path> - Save the screenshot",
            "  HELP - Show this message",
            "  EXIT - Disconnect"
        ]
        return "\n".join(help_text)
    
    elif command.startswith("copy "):
        paths = command[5:].strip()

        if ',' not in paths:
            return "Error: COPY command requires comma separator"

        parts = paths.split(',', 1)
        if len(parts) < 2:
            return ("Error: COPY command requires source and destination.\n"
                    "Usage: COPY C:\\source.txt,C:\\dest.txt")

        source_path = parts[0].strip()
        dest_path = parts[1].strip()

        if not os.path.exists(source_path):
            return f"Error: Source file not found: {source_path}"

        return copy_file_command(source_path, dest_path)

    elif command == "exit":
        return "Goodbye"

    else:
        return f"Unknown command: {command}"


def receive_message(client_socket):
    """Receives message with 4-byte length counter and verifies byte count"""
    length_data = client_socket.recv(4).decode()
    if not length_data:
        return None

    assert len(length_data) == 4, "Length data must be 4 bytes"
    expected_length = int(length_data)
    assert expected_length >= 0, "Expected length cannot be negative"
    logging.info(f"Client says they're sending {expected_length} bytes")

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
            f"Problem encounter: expected {expected_length} bytes "
            f"but got {actual_length}"
        )
        return None


def send_message(client_socket, message):
    """Sends message with 4-byte length prefix"""
    assert isinstance(message, str), "Message must be a string"
    
    message_bytes = message.encode()
    message_length = len(message_bytes)
    length_prefix = f"{message_length:04d}".encode()

    client_socket.send(length_prefix + message_bytes)
    logging.info(f"Sent {message_length} bytes to client")


def main():
    """
    This is where everything starts. It sets up the server and handles
    clients.

    Here's what happens:
    1. Creates a socket (think of it like a phone that can receive calls)
    2. Binds it to port 6000 (this is our phone number)
    3. Waits for clients to connect
    4. When a client connects, we receive their commands and send back
       responses
    5. When they disconnect, we wait for the next client

    The server runs forever until you stop it (Ctrl+C).
    It only handles one client at a time - if someone else tries to connect
    while we're busy, they have to wait.
    """

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    assert my_socket, "Failed to create socket"

    try:
        my_socket.bind(('0.0.0.0', 6000))
        my_socket.listen(QUEUE_LEN)
        logging.info("Server is listening on port 6000")

        while True:
            client_socket, client_address = my_socket.accept()
            assert client_socket, "Failed to accept client"
            logging.info(f"Connected by {client_address}")

            try:
                while True:
                    command = receive_message(client_socket)

                    if not command:
                        logging.info("Client disconnected")
                        break

                    logging.info(f'Received command: {command}')

                    try:
                        response = handle_command(command)
                        assert response, "Command processing failed"

                        send_message(client_socket, response)
                        logging.info(f'Sent response: {response}')

                        if command.lower() == "exit":
                            break
                    except Exception as e:
                        logging.error(f"Couldn't handle the command: {e}")

            except socket.error as err:
                logging.error(f'Received socket error on client socket: {err}')

            finally:
                client_socket.close()
                logging.info("Waiting for next client...")

    except socket.error as err:
        logging.error(f'Received socket error on server socket: {err}')

    finally:
        my_socket.close()
        logging.info("Server closed")


if __name__ == "__main__":
    main()