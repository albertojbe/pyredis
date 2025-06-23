import random
import socket
import threading

import resp_codec
storage = {}

def process(args):
    command = args[0].lower()
    match command:
        case "ping":
            return resp_codec.encode("PONG").encode()
        case "echo":
            if len(args) < 2:
                return resp_codec.encode(" ").encode()
            return resp_codec.encode(args[1]).encode()
        case "set":
            key = args[1]
            if key =="key:__rand_int__":
                key = random.randint(1, 20)
            value = args[2]
            if key in storage.keys():
                return resp_codec.encode("").encode()

            storage[key] = [value]
            return resp_codec.encode("OK").encode()
        case "get":
            key = args[1]
            if not key in storage.keys():
                return resp_codec.encode("").encode()
            if key =="key:__rand_int__":
                key = random.randint(1, 20)
            value = storage.get(key)
            return resp_codec.encode(value).encode()
        case "config":
            return resp_codec.encode([]).encode()
        case _:
            return resp_codec.encode(f'unknown command "{command}"', True).encode()

def handle_client(connection: socket, address):
    buffer = b""
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data

            while buffer:
                try:
                    frame, start = resp_codec.decode_frame(buffer)
                except resp_codec.IncompleteFrame:
                    break
                except Exception as e:
                    connection.sendall(resp_codec.encode(str(e), error=True).encode())
                    buffer = buffer[start:]
                    continue

                buffer = buffer[start:]
                connection.sendall(process(frame))
    finally:
        print(f"Connection with {address} closed")
        connection.close()

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        connection, address = server_socket.accept()
        print(f"Client {address} connected")
        buffer = b""
        threading.Thread(target=handle_client, args=(connection, address), daemon=True).start()

if __name__ == "__main__":
    main()
