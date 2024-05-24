import socket
import os

def handle_client(client_socket):
    try:
        # Receive the file name from the client
        file_name = client_socket.recv(1024).decode()
        if not file_name:
            return

        # Check if file exists
        if os.path.isfile(file_name):
            client_socket.send(b"EXISTS")
            with open(file_name, "rb") as f:
                while True:
                    file_data = f.read(1024)
                    if not file_data:
                        break
                    client_socket.send(file_data)
            client_socket.send(b"DONE")  # Indicate the end of the file transfer
        else:
            client_socket.send(b"ERROR")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen(1)
    print("Server listening on port 5000...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()
