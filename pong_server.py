import socket
#import time

HOST = "0.0.0.0"
PORT = 5000

def normalize(buf):
    return buf.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

def handle(conn, addr):
    print(f"Robot connected from {addr}")
    buffer = b""
    try:
        while True:
            try:
                chunk = conn.recv(1024)
            except OSError as e:
                print(f"Recv failed ({e}); robot likely disconnected.")
                return
            if not chunk:
                print("Robot disconnected.")
                return
            buffer = normalize(buffer + chunk)
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                msg = line.decode("ascii", errors="replace").strip()
                print(f"Received: {msg!r}")
                if msg == "PING":
                    #time.sleep(2)                     # simulated stall
                    try:
                        conn.sendall(b"PONG\n")
                        print("Sent: PONG")
                    except OSError as e:
                        print(f"Send failed ({e}); robot disconnected during stall.")
                        return                        # give up on this connection
    except OSError as e:
        print(f"Connection error with {addr}: {e}")
    finally:
        print(f"Closing connection to {addr}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Listening on {HOST}:{PORT}...")

    while True:                            # keep serving new connections
        conn, addr = server.accept()
        with conn:
            handle(conn, addr)


