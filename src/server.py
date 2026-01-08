"""HTTP forward proxy server with domain blocking and logging."""

import socket
import threading
from datetime import datetime
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "..", "logs", "proxy.log")
BLOCKED_FILE = os.path.join(BASE_DIR, "..", "config", "blocked_domains.txt")


def log_event(client_address, domain, action):
    """Write a single proxy event to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {client_address[0]}:{client_address[1]} | {domain} | {action}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(line)


def load_blocked_domains():
    """Load blocked domains from configuration file."""
    blocked = set()
    if os.path.exists(BLOCKED_FILE):
        with open(BLOCKED_FILE, "r", encoding="utf-8") as file:
            for line in file:
                domain = line.strip().lower()
                if domain:
                    blocked.add(domain)
    return blocked


def handle_client(client_socket, client_address, blocked_domains):
    """Handle a single client connection."""
    request_data = b""

    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        request_data += chunk
        if b"\r\n\r\n" in request_data:
            break

    request_text = request_data.decode(errors="ignore")

    host = None
    for line in request_text.split("\r\n"):
        if line.lower().startswith("host:"):
            host = line.split(":", 1)[1].strip().lower()
            break

    if host is None:
        client_socket.close()
        return

    domain = host.split(":")[0]

    # 🔴 BLOCKED DOMAIN HANDLING (VISIBLE OUTPUT)
    if domain in blocked_domains:
        body = "403 Forbidden: Domain is blocked by proxy\n"
        response = (
            "HTTP/1.1 403 Forbidden\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Content-Type: text/plain\r\n"
            "\r\n"
            f"{body}"
        )
        client_socket.sendall(response.encode())
        log_event(client_address, domain, "BLOCKED")
        client_socket.close()
        return

    lines = request_text.split("\r\n")
    request_line = lines[0]
    parts = request_line.split(" ")

    if len(parts) == 3 and parts[1].startswith("http"):
        url = parts[1][7:] if parts[1].startswith("http://") else parts[1]
        path = "/" + url.split("/", 1)[1] if "/" in url else "/"
        lines[0] = f"{parts[0]} {path} {parts[2]}"

    new_request_data = "\r\n".join(lines).encode()

    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((domain, 80))
        remote_socket.sendall(new_request_data)

        while True:
            response_chunk = remote_socket.recv(4096)
            if not response_chunk:
                break
            client_socket.sendall(response_chunk)

        remote_socket.close()
        log_event(client_address, domain, "ALLOWED")

    except (socket.error, OSError):
        log_event(client_address, domain, "ERROR")

    client_socket.close()


def start_server():
    """Start the proxy server and accept client connections."""
    blocked_domains = load_blocked_domains()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8888))
    server_socket.listen(50)

    print("Proxy server listening on 127.0.0.1:8888")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address, blocked_domains),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    start_server()
