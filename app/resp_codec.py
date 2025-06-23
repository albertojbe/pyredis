CRLF = "\r\n"

class RespError(Exception):
    pass

class _Reader:
    def __init__(self, message: str):
        self.message = message
        self.index = 0

    def read_line(self) -> str:
        end_of_line = self.message.find(CRLF, self.index)
        if end_of_line == -1:
            raise ValueError("RESP incompleto (CRLF faltando)")
        line = self.message[self.index:end_of_line]
        self.index = end_of_line + 2
        return line

    def read(self, position: int) -> str:
        if self.index + position > len(self.message):
            raise ValueError("Incomplete Message")
        text, self.index = self.message[self.index:self.index + position], self.index + position
        return text
    def __str__(self):
        return f"{self.message} {self.index}"

def decode(message: str or _Reader):
    if isinstance(message, str):
        message = _Reader(message)
    prefix: str = message.read(1)
    match prefix:
        case "+":
            return message.read_line()
        case "-":
            return RespError(message.read_line())
        case ":":
            return int(message.read_line())
        case "$":
            string_length = int(message.read_line())
            if string_length == -1:
                return None
            argument = message.read(string_length)
            if message.read(2) != CRLF:
                raise ValueError("Bulk String mal-formado (CRLF final faltando)")
            return argument
        case "*":
            array_length = int(message.read_line())
            arguments = []
            for x in range(array_length):
                arguments.append(decode(message))
            return arguments
    return None

def encode(message: str or list, error=False) -> str:
    if error:
        return f"-{message}\r\n"
    elif isinstance(message, str):
        return f"+{message}\r\n"
    elif isinstance(message, int):
        return f":{message}\r\n"
    elif isinstance(message, (list, tuple)):
        if len(message) == 1:
            text = message[0]
            text = f"${len(text)}\r\n{text}\r\n"
            return text
        text = f"*{len(message)}\r\n"
        for argument in message:
            text = text + f"${len(argument)}\r\n{argument}\r\n"

        return text
    return None


def main():
    print(decode("*1\r\n$4\r\nPING\r\n"))


if __name__ == "__main__":
    main()