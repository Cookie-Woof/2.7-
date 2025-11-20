



"""
Client and Server Program


This code allows the user to:
1. to work with files in the computer's local disc
the server knows to work with commands like
Excute, Take screenshot, save screenshot,
Dir, copy file and Exit.
for unknown commnads it helps the user to understand
what they can put in and what they cant and handles
empty/unknown command in a stedy way


2. handles more then one client,


Features:
- Handles unknown commands gracefully.
- Documents itself, showing what erorrs we stumbeled appon and the way
  of debug.
- Deals with unexpected erorrs
-


Arthur: Ariel Melamed Choen
Grade: 11th Grade 3rd class
Date: 14/11/2025


"""
import socket
import logging
import os # for delete
import glob # for DIR
import shutil # for copy
import pyautogui # for taking a screenshot
import sys
import subprocess #for excute


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


QUEUE_LEN = 1
MAX_PACKET = 1024




def takeScreenshot():
    """Take a screenshot and store it in memory."""
    global last_screenshot  # Access the global variable
    try:
        # Take the screenshot and store it
        last_screenshot = pyautogui.screenshot()
        
        # Get the size for confirmation
        width, height = last_screenshot.size
        
        return f"Screenshot captured sucssesfully!"
        
    except Exception as e:
        logging.error(f"Problem taking screenshot: {e}")
        return f"Error taking screenshot: {e}"




def save_screenshot(path):
    """Save the last screenshot to a file."""
    global last_screenshot
    try:
        # Check if there's a screenshot to save
        if last_screenshot is None:
            return "Error: No screenshot to save, Please use 'take screenshot' first!"
        
        last_screenshot.save(path, r'screen.jpg')
        
        return f"Screenshot saved to: {path}"
        
    except Exception as e:
        logging.error(f"Problem saving screenshot: {e}")
        return f"Error saving screenshot: {e}"




def dir_command(path):
    try:
        files_list = glob.glob(path + '\\*')
        
        if files_list:
            result = "Files found:\n" + "\n".join(files_list)
        else:
            result = f"No files found in {path}"
        
        return result
        
    except Exception as e:
        logging.error(f"Problem with dir command: {e}")
        return



def delete_command(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            # assert os.path.exists(path), "the file couldnt be removed"
            return f"File removed successfully! {path}"

        else:
            return f"Error: File not found: {path}"
    except Exception as e:
        logging.error(f"the file {path} couldnt be removed: {e}")
        return f"Error: Couldn't delete file: {e}"

    




def copy_file_command():
    #copy fileeeee
    print("copied the file!")




def excute_command():
    #amm excute the file
    print("huh")




def handle_command(command):
    """Handle incoming commands and return appropriate responses."""
    # Clean up the command
    command = command.strip().lower()
    # Check which command was sent
    if command.startswith("dir "):
        path = command[4:].strip()
        result = dir_command(path)
        return result
    
    elif command.startswith("take screenshot "):
        path = command[16:].strip()
        return takeScreenshot(path)
    
    elif command.startswith("save screenshot "):
        return save_screenshot()
    
    elif command.startswith("delete "):
        path = command[7:].strip()
        return delete_command(path)
    
    elif command.startswith("excute "):
        return excute_command()
    
    elif command == "exit":
        response = "Goodbye"
        return response
    else:
        return f"Unknown command: {command}"




def main():
    """Main server function."""
    # Create server socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    assert my_socket, "Failed to create socket"  # Assert 4


    try:
        # Bind to address and start listening
        my_socket.bind(('0.0.0.0', 6000))
        my_socket.listen(QUEUE_LEN)


        logging.info("Server is listening on port 6000")


        while True:  # Keep accepting new clients
            # Accept client connection
            client_socket, client_address = my_socket.accept()
            assert client_socket, "Failed to accept client"  # Assert 5
            logging.info(f"Connected by {client_address}")


            try:
                while True:  # Handle client commands
                    # Receive exactly 4 bytes
                    command = client_socket.recv(MAX_PACKET).decode().strip()
                   
                    # Check if client disconnected
                    if not command:
                        logging.info("Client disconnected")
                        break
                       
                    logging.info(f'Received command: {command}')
                   
                    try:
                        # Process command and send response
                        response = handle_command(command)
                        assert response, "Command processing failed"  # Assert 6
                       
                        client_socket.send(response.encode())
                        logging.info(f'Sent response: {response}')
                       
                        # Exit if client sent exit command
                        if command.lower() == "exit":
                            break
                    except Exception as e:
                        logging.error(f"couldnt handle the command {e}")


            except socket.error as err:
                logging.error(
                    f'Received socket error on client socket: {err}'
                )


            finally:
                # Close client connection
                client_socket.close()
                logging.info("Waiting for next client...")


    except socket.error as err:
        logging.error(f'Received socket error on server socket: {err}')


    finally:
        # Close server socket
        my_socket.close()
        logging.info("Server closed")




if __name__ == "__main__":
    main()