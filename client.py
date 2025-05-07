import socket
import threading
import time
import sys

def validate_request(line):
    parts = line.split(maxsplit=2)
    if len(parts) < 2:
        return False
    if parts[0].upper() == "PUT" and len(parts) < 3:
        return False
    combined = ' '.join(parts[1:])
    return len(combined) <= 970


def main():
    if len(sys.argv) != 4:
        print("Usage: client.py <host> <port> <request_file>")
        return

    host, port, file = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    
    try:
        with open(file) as f:
            requests = [line.strip() for line in f if line.strip()]
            print(f"Loaded {len(requests)} requests")
    except Exception as e:
        print(f"File error: {str(e)}")
        return

    with socket.socket() as s:
        try:
            s.connect((host, port))
            print(f"Connected to {host}:{port}")

            for req in requests:
                if not validate_request(req):
                    print(f"Invalid: {req}")
                    continue

                parts = req.split(maxsplit=2)
                op = parts[0].upper()
                key = parts[1]
                value = parts[2] if len(parts)>2 else ""

                cmd = {
                    "PUT": f"P {key} {value}",
                    "GET": f"G {key}",
                    "READ": f"R {key}"
                }.get(op, "")
                
                if not cmd:
                    print(f"Invalid operation: {req}")
                    continue
                
                msg_len = len(cmd)
                if msg_len > 999:
                    print(f"Oversized: {req}")
                    continue
                
                full_msg = f"{msg_len:03d}{cmd}"
                s.sendall(full_msg.encode())

                header = s.recv(3)
                if not header: 
                    print("Server disconnected")
                    break
                resp_len = int(header.decode())
                response = s.recv(resp_len).decode()
                print(f"{req} => {response}")

        except ConnectionRefusedError:
            print("Connection refused")
        except Exception as e:
            print(f"Connection error: {str(e)}")
            
if __name__ == "__main__":
    main()
        
    