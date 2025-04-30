import socket
import threading
import time

def client_task():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 51243))
        print("Connected to server")
    except Exception as e:
        print("Error connecting to server:", e)
    finally:
        client_socket.close()
        
def main():
    client = []
    for i in range(10):
        t = threading.Thread(target=client_task, args=(f"Client-{i+1}",))
        t.start()
        client.append(t)
        time.sleep(10)
        for t in client:
            t.join()
            
if __name__ == "__main__":
    main()
        
    