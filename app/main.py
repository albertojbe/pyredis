import random
import socket
import threading
import time

import resp_codec
storage = {}

def string_is_number(value: str):
    try:
        value = float(value)
        return True
    except ValueError:
        return False

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
                key = f"key:{random.randint(1, 10000)}"
            value = args[2]
            if key in storage.keys():
                return resp_codec.encode("").encode()

            storage[key] = {'value': [value], 'exp_at': None}

            if len(args) == 5:
                expiry_type = args[3].upper()
                expiry_time = args[4]
                match expiry_type:
                    case "EX":
                        storage[key]['exp_at'] = int(time.time() + int(expiry_time))
                    case "PX":
                        storage[key]['exp_at'] = int((time.time()) + (expiry_time / 1000))
                    case "EXAT":
                        storage[key]['exp_at'] = int(expiry_time)
                    case "PXAT":
                        storage[key]['exp_at'] = int(expiry_time / 1000)
            return resp_codec.encode("OK").encode()

        case "get":
            key = args[1]
            if not key in storage.keys():
                return resp_codec.encode("").encode()
            if key =="key:__rand_int__":
                key = f"key:{random.randint(1, 10000)}"
            expiry_date = storage[key]['exp_at']
            current_date = time.time()
            if expiry_date:
                if expiry_date < current_date:
                    del storage[key]
                    return resp_codec.encode("expired value").encode()

            value = storage[key]['value']
            return resp_codec.encode(value).encode()

        case "exists":
            if args[1] in storage.keys():
                return resp_codec.encode(1).encode()
            return resp_codec.encode(0).encode()

        case "del":
            count = 0
            for key in args[1:]:
                if key in storage.keys():
                    del storage[key]
                    count += 1
            return resp_codec.encode(count).encode()

        case "incr":
            print(storage)
            key = args[1]
            if key in storage.keys():
                value = storage[key]['value']
                if string_is_number(value):
                    value = float(value) + 1
                    storage[key]['value'] = str(value)
                    return resp_codec.encode(int(value)).encode()
                storage[key]['value'] = str(1)
                return resp_codec.encode(1).encode()
            storage[key]= {'value':str(1), 'exp_at':None}
            return resp_codec.encode(1).encode()

        case "decr":
            key = args[1]
            if key in storage.keys():
                value = storage[key]['value']
                if string_is_number(value):
                    value = float(value) - 1
                    storage[key]['value'] = str(value)
                    return resp_codec.encode(int(value)).encode()
                storage[key]['value'] = str(1)
                return resp_codec.encode(1).encode()
            storage[key]['value'] = str(1)
            return resp_codec.encode(1).encode()



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
