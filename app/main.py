import socket
import resp_codec

def main():
    storage = {}
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        connection, address = server_socket.accept()
        print(f"Client {address} connected")
        data = connection.recv(1024)
        print(data)
        arguments = resp_codec.decode(data.decode())
        command = arguments[0].lower()
        match command:
            case "ping":
                connection.sendall(resp_codec.encode(["PONG"]).encode())
            case "set":
                key = arguments[1]
                value = arguments[2]
                if key in storage.keys():
                    connection.sendall(resp_codec.encode("").encode())
                    continue
                storage[key] = [value]
                connection.sendall(resp_codec.encode("OK").encode())
            case "get":
                key = arguments[1]
                if not key in storage.keys():
                    connection.sendall(resp_codec.encode("").encode())
                    continue
                value = storage.get(arguments[1])
                connection.sendall(resp_codec.encode(value).encode())
            case _:
                connection.sendall(resp_codec.encode(f"ERR unknown command {command}").encode())
if __name__ == "__main__":
    main()
