#Authors
# Siyamthanda Ndlovu - 21582735 
# Katlego Zondo - 21
import socket
import random
import time


class client():
    """ Initialises variables """
    def __init__(self,id,name):
        self.id=None

    def print(self):
        """ Prints individual client """
        result = "{self.id}"
        return result


class fibonacci_server :
    """ Initialises variables """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_list = {}

    def start(self):
        """ Starts the server """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print(f"Fibonacci server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from {client_address[0]}:{client_address[1]}")

            # Handle client connection here

            client_socket.close()

    def stop(self):
        """ Stops the server """
        if self.server_socket:
            self.server_socket.close()
    
    def add_new_client(client):
        


    def generate_new_id(self):
        """ Generate new ID for new connection """
        id = int(time.time() * 1000)
        return id

    def print_clients(self):
        """ Prints all client """
        result = ""
        for client in self.client_list :
            result += client.print() + "\n"

        return result




    

# Example usage
server =fibonacci_server("localhost", 8080)
server.start()

