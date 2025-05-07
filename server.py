import socket
import threading
import time

tuple_space = {}
lock = threading.Lock()
states = {
    'reads': 0,
    'gets': 0,
    'puts': 0,
    'total_clients': 0,
    'total_operations': 0,
    'errors': 0
}
def put(k,v):
    with lock:
        states['puts'] += 1
        if k in tuple_space:
            states['errors'] += 1
            return f"ERR {k} already exists"
        tuple_space[k] = v
        return f"OK({k},{v})added"
def get(k):
    with lock:
        states['gets'] += 1
        if k in tuple_space:
            v = tuple_space.pop(k)
            return f"OK({k},{v})removed"
        else:
            states['errors'] += 1
            return f"ERR {k} does not exist"
def read(k):
    with lock:
        states['reads'] += 1
        if k in tuple_space:
            return f"OK({k},{tuple_space[k]})read"
        else:
            states['errors'] += 1
            return f"ERR {k} does not exist"
def handle_client(client_socket,addr):
    global states
    with lock:
        states['total_clients'] += 1
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            header = client_socket.recv(3)
            if len(header) != 3:
                return
            msg_len = int(header.decode('utf-8'))
            message = b''
            while len(message) < msg_len:
                chunk = client_socket.recv(msg_len - len(message))
                if not chunk:
                    break
                message += chunk
            decode_message = message.decode('utf-8')
            print(f"Received from {addr}: {decode_message}")
            parts = decode_message.split(maxsplit=2)
            operation = parts[0]
            k = parts[1]
            v = parts[2] if len(parts) > 2 else ""
            with lock:
                states['total_operations'] += 1
                if operation == "PUT":
                    response = put(k,v)
                elif operation == "GET":
                    response = get(k)
                elif operation == "READ":
                    response = read(k)
                else:
                    response = "ERR Invalid operation."
                    states['errors'] += 1
            formatted_response = f"{len(str(response)):03d}{response}"
            client_socket.send(formatted_response.encode('utf-8'))
    finally:
        client_socket.close()
def states_monitor():
    while True:
        time.sleep(10)
        with lock:
            total_size = sum(len(k)+len(v) for k, v in tuple_space.items())
            count = len(tuple_space)
            avg_size = total_size/count if count > 0 else 0
            avg_key = sum(len(k) for k in tuple_space)/count if count > 0 else 0
            avg_val = sum(len(v) for v in tuple_space.values())/count if count > 0 else 0
            
            print (
                f"Tuples: {count} | Avg size: {avg_size:.1f} | "
                f"Avg key: {avg_key:.1f} | Avg value: {avg_val:.1f} | "
                f"Clients: {states['total_clients']} | Ops: {states['total_operations']} | "
                f"READs: {states['reads']} | GETs: {states['gets']} | "
                f"PUTs: {states['puts']} | Errors: {states['errors']}"
            )
    
    
def start_server():
    host = "127.0.0.1"
    port = 51234
    
    serve_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serve_socket.bind((host, port))
    serve_socket.listen(5)
    
    print("Server is running and ready to accept multiple clients...")
    
    states_thread = threading.Thread(target=states_monitor)
    states_thread.start()
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
        