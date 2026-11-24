import socket
import random
import threading

Host = 'localhost'
Port = 5001

Server_name = "Server of Mouneim"

# Event used to signal server shutdown
Stop_event = threading.Event()

# Function executed by each client thread
def Handle_client(Client_socket, Client_address):

    print(f"Connection established with {Client_address}")

    try:
        # Receiving the client's message
        message = Client_socket.recv(1024).decode()

        Client_name, Client_number = message.split(" : ")
        Client_number = int(Client_number)

        # Shutdown rule
        if not 1 <= Client_number <= 100:
            Client_socket.sendall(
                "Invalid input. Please send an integer between 1 and 100.".encode()
            )

            print(f"Invalid number received from {Client_address}")
            Stop_event.set()
            return

        # Display client and server names
        print("Client name:", Client_name)
        print("Server name:", Server_name)

        # Generate a random number
        Server_number = random.randint(1, 100)

        # Calculate the sum
        total_sum = Client_number + Server_number

        # Display results
        print(f"The client's integer: {Client_number}")
        print(f"The server's integer: {Server_number}")
        print(f"The sum of both integers: {total_sum}")

        # Send response to the client
        response = f"{Server_name} : {Server_number}"

        Client_socket.sendall(response.encode())

        print(f"Response sent to {Client_address}")

    except Exception as e:
        print(f"Error with client {Client_address}: {e}")

    finally:
        # Close this client's socket
        Client_socket.close()
        print(f"Connection closed with {Client_address} \n")


# Create the welcoming socket
Server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Bind and listen
    Server_socket.bind((Host, Port))
    Server_socket.listen()

    # Allow accept() to periodically check the shutdown event
    Server_socket.settimeout(0.5)

    print(f"{Server_name} is listening on {Host}:{Port}")

    # Accept multiple clients
    while not Stop_event.is_set():

        try:
            Client_socket, Client_address = Server_socket.accept()

            if Stop_event.is_set():
                Client_socket.close()
                break

            # Create a new thread for each client
            Client_thread = threading.Thread(
                target=Handle_client,
                args=(Client_socket, Client_address)
            )

            # Start the thread
            Client_thread.start()

            print("New client thread started!")

        except socket.timeout:
            continue

finally:
    # Close the welcoming socket
    Server_socket.close()
    print("Server socket closed. Server terminated.")