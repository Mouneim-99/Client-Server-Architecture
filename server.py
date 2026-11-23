import socket
import random

Host = 'localhost'
Port = 5001

Server_name = "Server of Mouneim"

Server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
#listening 
    Server_socket.bind((Host, Port))
    Server_socket.listen()
    print(f"Server {Server_name} is listening on {Host}:{Port}")

#Accepting the connection from the client :
    while True:
        Client_socket , Client_address = Server_socket.accept()
        print(f"Connection established with {Client_address}")

        try:
            message = Client_socket.recv(1024).decode()
            Client_name, Client_number = message.split(" : ")

#shutdown rule :
            if not 1 <= int(Client_number) <= 100:
                Client_socket.send("Invalid input. Please send an integer between 1 and 100.".encode())
                Client_socket.close()
                break

            Client_number = int(Client_number)

#Display :
            print("Client name :", Client_name)
            print("Server name :", Server_name)

#Picking a random number between 1 and 100 :
            Server_number = random.randint(1, 100)

#Calculating the sum of both integers :
            total_sum = Client_number + Server_number
            print(f"The client's integer : {Client_number} \nThe server's integer : {Server_number} \nThe sum of both integers : {total_sum}")

#Sending the response back to the client :
            response = f"{Server_name} : {Server_number}"

            Client_socket.send(response.encode())
            print("Response sent successfully")

        finally:
            Client_socket.close()
finally:
    Server_socket.close()
    print("Server socket closed")