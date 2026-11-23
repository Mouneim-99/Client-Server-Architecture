import socket

Host = 'localhost'
Port = 5001

Client_name ="Client of Mouneim"

while True:
    try:
        number = int(input("Enter a number between 1 and 100 :"))
        if 1 <= number <= 100:
            break
        else:
            print("Error , The number must be between 1 and 100")
    except ValueError:
        print("Error , Please enter a valid number")
    
Client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :
    Client_socket.connect((Host, Port))
    print("Connected to the server successfully")
#sending the message :
    message = f"{Client_name} : {number}"
    Client_socket.send(message.encode())
    print("Message sent to the server successfully")
#receiving the response :
    response = Client_socket.recv(1024).decode()

#Extracting the server informations :
    Server_name, server_number = response.split(" : ")
    server_number = int(server_number)

#Display :
    print("Client name :", Client_name)
    print("Server name :", Server_name)

    print(f"The sum of both integers is : {number + server_number}")

except Exception as e:
    print("Error occurred while connecting to the server:", str(e))
finally:
    Client_socket.close()
    print("Connection closed")
    

