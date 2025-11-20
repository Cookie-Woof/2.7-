"""
Client Program


Connects to the server and sends 4-byte commands.


Author: Ariel Melamed Choen
Grade: 11th Grade 3rd class
Date: 1/11/2025
"""
import socket
import logging



IP = "192.168.50.104"
PORT = 6000


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
""""make the function, handle the data, squnce diagram, start writing the code of the server and the protocol also the server and then like make a place for all of the assertes and stuff dont put assertes on the conctions and stuff for somre reason we need to put them for the code and stuff"""
MAX_PACKET = 1024


def main():
    """Main client function."""
    # Create client socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    assert my_socket, "Failed to create socket"  # Assert 1


    try:
        # Connect to server
        my_socket.connect((IP, PORT))
        logging.info("Connected to server")
       
        try:
            while True:  # Keep asking for commands
                msg = input("Enter command: ")
                assert isinstance(msg, str), "Input must be a string"  # Assert 2
                # Send command to server
                my_socket.send(msg.encode())
                logging.info(f"Sent command: {msg}")
               
                # Receive response from server
                response = my_socket.recv(1024).decode()
                assert response, "No response received from server"  # Assert 4
                assert isinstance(response, str), "Response must be a string"  # Assert 5
               
                logging.info(f"Received response: {response}")
                print("Server:", response)
                   
                    # Exit if user typed exit
                if msg.lower() == "exit":
                    assert msg.lower() == "exit", "Exit command verification failed"  # Assert 6
                    logging.info("Exiting client")
                    break
        except Exception as e:
            logging.error(f"couldnt input/resive {e}")
           
    except socket.error as err:
        logging.error(f'Received socket error: {err}')


    finally:
        # Close connection
        my_socket.close()
        logging.info("Connection closed")




if __name__ == "__main__":
    main()


