# Design Document – Custom Network Proxy Server

## 1. Overview

This document describes the design and architecture of the Custom Network Proxy Server.
The proxy acts as an intermediary between clients and destination servers, forwarding HTTP
requests and relaying responses while enforcing domain-based filtering and logging.

The design focuses on correctness, simplicity, and clarity rather than production-scale optimization.

---

## 2. High-Level Architecture

The system follows a classic client–proxy–server architecture:

Client → Proxy Server → Destination Server  
Destination Server → Proxy Server → Client

The proxy listens for incoming client connections, processes HTTP requests, applies filtering
rules, forwards allowed requests, and streams responses back to the client.

---

## 3. Major Components

### 3.1 Connection Listener

- Creates a TCP socket bound to a fixed address and port
- Listens for incoming client connections
- Accepts connections in a loop

### 3.2 Client Handler

- Each client connection is handled independently
- Reads incoming HTTP requests
- Parses request headers
- Applies filtering logic
- Forwards requests or blocks them
- Sends responses back to the client

### 3.3 Request Parser

- Reads HTTP request data until the header terminator (`\r\n\r\n`)
- Extracts:
  - HTTP method
  - Request target
  - Host header
- Converts absolute URLs into relative paths for forwarding

### 3.4 Domain Filter

- Loads blocked domains from a configuration file at startup
- Normalizes hostnames (lowercasing)
- Compares requested domain against blocked list
- Blocks requests by returning HTTP 403 Forbidden

### 3.5 Forwarding Engine

- Opens a TCP connection to the destination server
- Forwards the modified HTTP request
- Streams response data back to the client without buffering entire responses

### 3.6 Logger

- Records each request event to a log file
- Logs include:
  - Timestamp
  - Client IP and port
  - Requested domain
  - Action taken (ALLOWED / BLOCKED / ERROR)

---

## 4. Concurrency Model

### Model Used: Thread-per-Connection

- Each incoming client connection is handled by a separate thread
- Threads are lightweight and suitable for moderate workloads
- This model is simple to implement and debug

### Rationale

- Explicitly allowed by the project requirements
- Avoids complexity of event-driven models
- Suitable for educational and demonstration purposes

---

## 5. Request Handling Flow

1. Client establishes a TCP connection to the proxy
2. Proxy accepts the connection
3. A new thread is spawned for the client
4. Proxy reads the HTTP request headers
5. Host header is extracted
6. Domain is checked against the blocked list
7. If blocked:
   - Proxy returns HTTP 403 Forbidden
   - Event is logged
8. If allowed:
   - Proxy connects to destination server
   - Request is forwarded
   - Response is streamed back to the client
   - Event is logged
9. Connections are closed cleanly

---

## 6. Error Handling

- Invalid or malformed requests are safely ignored
- Missing Host headers result in connection termination
- Network errors are caught and logged
- Proxy continues running even if individual requests fail

The design ensures that no single client error crashes the server.

---

## 7. Logging Strategy

- Logging is file-based and persistent
- Each request generates exactly one log entry
- Log format is consistent and human-readable
- Logs serve as both debugging aids and test artifacts

---

## 8. Configuration Management

- Blocked domains are stored in an external configuration file
- Configuration is loaded once at server startup
- Changes require a server restart
- This approach simplifies implementation and avoids runtime overhead

---

## 9. Security Considerations

- The proxy does not inspect encrypted HTTPS traffic
- No authentication or authorization is implemented
- Input is minimally validated to prevent crashes
- Designed for controlled environments, not production deployment

---

## 10. Limitations

- HTTPS CONNECT tunneling not implemented
- No response caching
- No authentication mechanism
- Hardcoded listening address and port
- No dynamic configuration reload

These limitations are intentional to keep the design simple and focused.

---

## 11. Conclusion

The proxy server successfully demonstrates core networking and systems concepts,
including socket programming, concurrency, HTTP request handling, filtering, and logging.
The design prioritizes clarity, correctness, and alignment with project requirements.
