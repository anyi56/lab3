import socket
import threading

tuple_space = {}
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
def put(k,v):
    global tuple_space
    if k in tuple_space:
        print(f"ERR {k} already exists")
    else:
        tuple_space[k] = v
        print(f"OK({k},{v})added")
def get(k):
    global tuple_space
    if k in tuple_space:
        print(f"OK({k},{v})removed")
        del tuple_space[k]
    else:
        print(f"ERR {k} does not exist")
def read(k):
    global tuple_space
    if k in tuple_space:
        print(f"OK({k},{v})read")
    else:
        print(f"ERR {k} does not exist")
    
    
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
        