import os
import hashlib
import socket
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
FTP_SERVER = 'localhost'
FTP_PORT = 21
FTP_USER = 'ftpuser'
FTP_PASS = 'katnicole'
REMOTE_FILE_PATH = '/home/ftpuser/ftp/files/good_file.txt'

LOCAL_FILE_PATH = REMOTE_FILE_PATH





POLL_INTERVAL = 10  # seconds

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def compute_md5(file_path):
    """Compute the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def send_command(ftp_socket, cmd):
    """Send a command to the FTP server and return the response."""
    ftp_socket.sendall((cmd + '\r\n').encode())
    return ftp_socket.recv(1024).decode()

def download_file():
    """Download the remote file via FTP."""
    logging.info("Connecting to FTP server...")
    print("Connecting to FTP server...")  # Add print statement
    ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ftp_socket.connect((FTP_SERVER, FTP_PORT))
    ftp_socket.recv(1024)  # Welcome message

    # Login
    send_command(ftp_socket, f'USER {FTP_USER}')
    send_command(ftp_socket, f'PASS {FTP_PASS}')

    # Switch to binary mode
    send_command(ftp_socket, 'TYPE I')

    # Enter passive mode
    pasv_response = send_command(ftp_socket, 'PASV')
    logging.debug(f"PASV response: {pasv_response}")

    # Print the PASV response
    print("PASV response:", pasv_response)

    # Parse PASV response to get data connection details
    start = pasv_response.find('(') + 1
    end = pasv_response.find(')')
    numbers = pasv_response[start:end].split(',')
    ip = '.'.join(numbers[:4])
    port = (int(numbers[4]) << 8) + int(numbers[5])

    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((ip, port))

    # Retrieve the file
    send_command(ftp_socket, f'RETR {REMOTE_FILE_PATH}')

    with open(LOCAL_FILE_PATH, 'wb') as f:
        while True:
            data = data_socket.recv(1024)
            if not data:
                break
            f.write(data)

    data_socket.close()
    send_command(ftp_socket, 'QUIT')
    ftp_socket.close()
    logging.info("File downloaded successfully.")

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, monitored_file, known_good_hash):
        self.monitored_file = monitored_file
        self.known_good_hash = known_good_hash

    def on_modified(self, event):
        print("File modified event detected.")
        if event.src_path == self.monitored_file:
            print(f"Detected modification in {self.monitored_file}")
            self.check_and_restore_file()

    def check_and_restore_file(self):
        print("Checking and restoring file...")
        if os.path.exists(self.monitored_file):
            print("File exists.")
            current_hash = compute_md5(self.monitored_file)
            print("Current hash:", current_hash)
            if current_hash != self.known_good_hash:
                print("File has been altered, restoring the known-good file...")
                download_file()
                self.known_good_hash = compute_md5(self.monitored_file)
                print("File restored successfully.")
        else:
            print("File does not exist.")


def main():
    # Ensure the local file exists and get its initial hash

  
    if not os.path.exists(LOCAL_FILE_PATH):
        logging.info(f"{LOCAL_FILE_PATH} does not exist. Downloading the initial file...")
        download_file()

    known_good_hash = compute_md5(LOCAL_FILE_PATH)
    logging.info(f"Initial hash of the protected file: {known_good_hash}")

    event_handler = FileMonitorHandler(LOCAL_FILE_PATH, known_good_hash)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(LOCAL_FILE_PATH), recursive=False)
    observer.start()
    
    print("File monitoring started.") 

    try:
        while True:
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
