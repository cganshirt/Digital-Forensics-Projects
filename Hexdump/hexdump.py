import os
import sys


def get_hexdump(file: str):
    """Opens file and prints hexdump line by line until there are no more bytes to be read"""
    filesize = os.path.getsize(file)
    if filesize == 0:
        return
    with open(file, "rb") as filedes:
        offset = 0
        while True:
            data = filedes.read(16)
            if len(data) < 16:
                # if theres no more data return the current offset and break
                if len(data) == 0:
                    print("{:08x}".format(offset))
                    break
                # otherwise run format_data once more, print offset and break
                else:
                    format_data(data, offset)
                    offset += len(data)
                    print("{:08x}".format(offset))
                    break
            format_data(data, offset)
            offset += 16


def format_data(data: bytes, offset: int):
    """Takes the data read in and outputs the next line of the hexdump"""
    text = "".join([chr(i) if ord(chr(i)) > 31 and ord(chr(i)) < 127
                    else "." for i in data])
    hex = "{:08x}".format(offset) + "  "
    hex += " ".join("{:02x}".format(ord(chr(i))) for i in data[:8])
    hex += "  "
    hex += " ".join("{:02x}".format(ord(chr(i))) for i in data[8:])
    # check to make sure that there are 16 bytes being read
    if len(data) % 16 != 0:
        offset += len(data)
        # if data is less than or equal to 8 bytes account for the double
        # spacing at the 8 byte mark
        if len(data) <= 8:
            hex += "   " * (16 - len(data)) + " |" + text + "|"
        else:
            hex += "   " * (16 - len(data)) + "  |" + text + "|"
    else:
        hex += "  " + "|" + text + "|"
    print(hex)


if __name__ == "__main__":
    file = sys.argv[1]
    get_hexdump(file)
