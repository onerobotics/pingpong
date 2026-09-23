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
            chunk = conn.recv(1024)
            if not chunk:                      # empty bytes = peer closed
                print("Robot disconnected.")
                return
            print(f"Raw: {chunk!r} [{chunk.hex(' ')}]")
            buffer = normalize(buffer + chunk)

            # A single recv may contain 0, 1, or several messages - or a
            # partial one. Pull out every complete (newline-terminated) message
            # and leave any partial remainder in the buffer for next time.
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                msg = line.decode("ascii", errors="replace").strip()
                print(f"Received: {msg!r}")
                if msg == "PING":
                    #time.sleep(2)              # simulated stall
                    conn.sendall(b"PONG\n")
                    print("Sent: PONG")
                else:
                    conn.sendall(b"ERR unknown\n")
    except OSError as e:                       # recv or send failed: robot hung up
        print(f"Connection error with {addr}: {e}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Listening on {HOST}:{PORT}...")

    while True:                            # keep serving new connections
        conn, addr = server.accept()
        with conn:
            handle(conn, addr)
