import random
import socket
import resp_codec
storage = {}

def process(args):
    command = args[0].lower()
    print(args)
    match command:
        case "ping":
            return resp_codec.encode("PONG").encode()
        case "echo":
            if len(args) < 2:
                return resp_codec.encode(" ").encode()
            return resp_codec.encode(args[1]).encode()
        case "set":
            print(storage)
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

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        connection, address = server_socket.accept()
        print(f"Client {address} connected")
        buffer = b""
        while True:
            data = connection.recv(4096)
            if not data:
                break

            buffer += data
            print(buffer)
            try:
                while buffer:
                    try:
                        frame, used = resp_codec.decode_frame(buffer)
                    except resp_codec.IncompleteFrame:
                        break
                    except Exception as e:
                        connection.sendall(resp_codec.encode(str(e), error=True).encode())
                        buffer = buffer[used:]
                        continue
                    buffer = buffer[used:]
                    reply = process(frame)
                    connection.sendall(reply)
            except Exception as e:
                print("Erro no decode:", e)
                connection.sendall(resp_codec.encode("ERR decoding", True).encode())
                continue

if __name__ == "__main__":
    main()