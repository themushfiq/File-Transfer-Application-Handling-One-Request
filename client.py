import socket
import os

def download_file(server_ip, file_name):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 5000))

    client.send(file_name.encode())

    response = client.recv(1024)
    if response == b"EXISTS":
        with open(os.path.join("downloads", file_name), "wb") as f:
            while True:
                file_data = client.recv(1024)
                if file_data == b"DONE":
                    break
                f.write(file_data)
        print(f"Downloaded {file_name}")
    else:
        print(f"File '{file_name}' not found on the server.")

    client.close()

def main():
    server_ip = input("Enter server IP address: ")  # Prompt for the server IP address
    os.makedirs("downloads", exist_ok=True)  # Ensure the downloads directory exists

    while True:
        file_name = input("Enter the name of the file to download (or 'exit' to quit): ")
        if file_name.lower() == 'exit':
            break
        download_file(server_ip, file_name)

if __name__ == "__main__":
    main()
