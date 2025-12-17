# 2.7-
This code includes a protocol that has the job of verifying if the amount of bytes that the client has sent to the server, for example: 
Server: Enter command: 

Client: "take screenshot".

So the amount of bytes that the client sends for this instance is 15 bytes, so what this protocol does is verify with the client and server that we're all in the same line and that the server got all of the 15 bytes, as expected from the server's side:


2025-12-17 12:18:39,539 - INFO - Client says they're sending 15 bytes

2025-12-17 12:18:39,540 - INFO - Verified: received 15 bytes (matches expected)



and as a respond to the command the client sent, the server does the same:

2025-12-17 12:18:39,592 - INFO - Sent 61 bytes to client

2025-12-17 12:18:39,593 - INFO - Sent response: Screenshot captured! Use 'save screenshot <path>' to save it. 



