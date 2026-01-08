# Custom Network Proxy Server

## Project Overview
This project implements a custom forward HTTP proxy server using TCP sockets.
The proxy accepts client HTTP requests, forwards them to destination servers,
and relays responses back to clients.

The project demonstrates core systems and networking concepts such as socket
programming, concurrency, HTTP request parsing, request forwarding, and logging.

---

## Features
- TCP-based HTTP forward proxy
- Concurrent client handling using threads
- HTTP request parsing and forwarding
- Domain-based blocking using configuration file
- Persistent logging of requests
- Streaming responses without buffering entire content

---

## Technologies Used
- Python 3
- Socket programming
- Threading
- HTTP protocol

---

## Project Structure
```
proxy-project/
├── src/
│ └── server.py
├── config/
│ └── blocked_domains.txt
├── logs/
│ └── proxy.log
├── tests/
│ ├── test_commands.txt
│ └── sample_logs.txt
├── docs/
│ └── design.md
└── README.md
```
---

## Configuration
Blocked domains are listed in:
```
config/blocked_domains.txt
```

Each line contains one domain name to block.  
Changes to this file require restarting the proxy server.

---

## How to Run the Project
1. Navigate to the project root directory
2. Start the proxy server:
```
python src/server.py
```

3. Send HTTP requests through the proxy:
```
curl.exe -x http://localhost:8888 http://example.com
```
---

## Logging
All requests are logged to:
```
logs/proxy.log
```

Log format:
```
TIMESTAMP | CLIENT_IP:PORT | DOMAIN | ACTION
```
---

## Testing
Test commands are provided in:
```
tests/test_commands.txt
```

Sample logs generated during testing are available in:
```
tests/sample_logs.txt
```
Malformed HTTP requests were tested to ensure the proxy handles invalid input without crashing.
---

## Limitations
- HTTPS CONNECT tunneling not implemented
- No caching
- No authentication

---

## Author
Name: SARTHAK CHANDEL  
Department: Geophysical Technology 

Enrollment No.: 23411033
