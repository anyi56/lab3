import socket
import threading

def handle_client(client_socket,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    message = client_socket.recv(1024).decode('utf-8')
    parts = message.split()
    operation = parts[0]
    k = parts[1]
    v = parts[2]    
    if operation == "PUT":
        put(k,v)
    elif operation == "GET":
        get(k)
    elif operation == "READ":
        read(k)
    else:
        print("Invalid operation.")
    def read():
        while True:
            try:
                if message:
                    print(f"{addr} : {message}")
                else:
                    print(f"{addr} disconnected.")
                    break
            except:
                print(f"{addr} disconnected.")
                break
    def get():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
            except:
                print(f"{addr} disconnected.")
                break
    def put():
        while True:
            try:
                message = input()
                client_socket.send(message.encode('utf-8'))
            except:
                print(f"{addr} disconnected.")
                break
    
def start_server():
    host = "127.0.0.1"
    port = 51234
    
    serve_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serve_socket.bind((host, port))
    serve_socket.listen(5)
    
    print("Server is running and ready to accept multiple clients...")
    
    try:
        while True:
            client_socket, addr = serve_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        serve_socket.close()
        
if __name__ == "__main__":
    start_server()
        