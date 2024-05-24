Report on File Transfer Application Handling One Request at a Time

Abstract
This report presents the design, implementation, and testing of a simple file transfer application developed using Python. The application handles file transfer requests one at a time, ensuring efficient and reliable transmission of files from a server to a client. The server listens for incoming connections and responds to file requests, while the client sends file requests and receives the corresponding files. This application was developed and tested using PyCharm IDE.

Introduction
File transfer applications are essential for sharing files over a network. This project aims to develop a straightforward file transfer application that handles one request at a time. The focus is on simplicity and reliability, ensuring that files can be transferred from the server to the client without errors. This application consists of two main components: the server and the client.

Objectives
1.	To develop a server application that listens for incoming connections and handles file transfer requests.
2.	To develop a client application that connects to the server, requests a file, and downloads it.
3.	To ensure the file transfer process is reliable and efficient.

System Design
Server
The server application is designed to:
1.	Listen for incoming connections on a specified port.
2.	Accept a connection from a client.
3.	Receive the file name requested by the client.
4.	Check if the requested file exists.
5.	Send the file to the client if it exists or an error message if it does not.


Client
The client application is designed to:
1.	Connect to the server using the server's IP address and port number.
2.	Send a file request to the server.
3.	Receive the requested file from the server and save it locally.
4.	Display appropriate messages based on the server's response.

Implementation
The application was implemented in Python using the socket module for network communication and the os module for file operations.

Server Code: 
1.	import socket
2.	import os
3.	
4.	def handle_client(client_socket):
5.	    try:
6.	        # Receive the file name from the client
7.	        file_name = client_socket.recv(1024).decode()
8.	        if not file_name:
9.	            return
10.	
11.	        # Check if file exists
12.	        if os.path.isfile(file_name):
13.	            client_socket.send(b"EXISTS")
14.	            with open(file_name, "rb") as f:
15.	                while True:
16.	                    file_data = f.read(1024)
17.	                    if not file_data:
18.	                        break
19.	                    client_socket.send(file_data)
20.	            client_socket.send(b"DONE")  # Indicate the end of the file transfer
21.	        else:
22.	            client_socket.send(b"ERROR")
23.	    except Exception as e:
24.	        print(f"Error: {e}")
25.	    finally:
26.	        client_socket.close()
27.	
28.	def main():
29.	    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
30.	    server.bind(("0.0.0.0", 5000))
31.	    server.listen(1)
32.	    print("Server listening on port 5000...")
33.	
34.	    while True:
35.	        client_socket, addr = server.accept()
36.	        print(f"Accepted connection from {addr}")
37.	        handle_client(client_socket)
38.	
39.	if __name__ == "__main__":
40.	    main()
41.	

Client Code:
1.	import socket
2.	import os
3.	
4.	def download_file(server_ip, file_name):
5.	    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
6.	    client.connect((server_ip, 5000))
7.	
8.	    client.send(file_name.encode())
9.	
10.	    response = client.recv(1024)
11.	    if response == b"EXISTS":
12.	        with open(os.path.join("downloads", file_name), "wb") as f:
13.	            while True:
14.	                file_data = client.recv(1024)
15.	                if file_data == b"DONE":
16.	                    break
17.	                f.write(file_data)
18.	        print(f"Downloaded {file_name}")
19.	    else:
20.	        print(f"File '{file_name}' not found on the server.")
21.	
22.	    client.close()
23.	
24.	def main():
25.	    server_ip = input("Enter server IP address: ")  # Prompt for the server IP address
26.	    os.makedirs("downloads", exist_ok=True)  # Ensure the downloads directory exists
27.	
28.	    while True:
29.	        file_name = input("Enter the name of the file to download (or 'exit' to quit): ")
30.	        if file_name.lower() == 'exit':
31.	            break
32.	        download_file(server_ip, file_name)
33.	
34.	if __name__ == "__main__":
35.	    main()

Testing and Results
The application was tested in a local network environment. The server was started on a machine with a specified IP address, and the client was run on a different machine within the same network.

Test Cases
1.	File Exists on Server: The client requests a file that exists on the server. The server successfully sends the file, and the client downloads it without errors.
2.	File Does Not Exist on Server: The client requests a file that does not exist on the server. The server responds with an error message, and the client displays an appropriate message.
3.	Multiple Requests: The client sends multiple file requests one after the other. Each request is handled successfully, demonstrating that the server can process one request at a time sequentially.
Results
The application performed as expected. Files were transferred correctly when they existed on the server, and appropriate error messages were displayed when files did not exist. The server successfully handled multiple sequential requests from the client.

Conclusion
The file transfer application developed in this project is a simple yet effective solution for transferring files over a network. By handling one request at a time, the application ensures reliable file transmission. The implementation using Python and the socket module is straightforward and demonstrates the fundamental concepts of network communication and file handling.


Future Work
Future improvements to the application could include:
1.	Implementing concurrency to handle multiple requests simultaneously.
2.	Adding encryption to secure file transfers.
3.	Developing a graphical user interface (GUI) for ease of use.
4.	Implementing more robust error handling and logging mechanisms.
   
References
1.	Python socket module documentation: https://docs.python.org/3/library/socket.html
2.	Python os module documentation: https://docs.python.org/3/library/os.html
