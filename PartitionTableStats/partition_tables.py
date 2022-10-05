import uuid


def parse_mbr(mbr_bytes: bytes) -> list[dict]:
    """Parses the MBR partitions and returns the type, start, end and number for each"""
    partitionList = []
    # iterates through for possible partitions
    for i in range(4):
        # the information we need to output starts at byte 450 for each 16 byte partition
        partitionType = mbr_bytes[450 + (i * 16)]
        if partitionType == 0:
            continue
        start = 450 + (i * 16)
        end = start + 12
        partition = mbr_bytes[start:end]
        partitionStart = int.from_bytes(partition[4:7], "little")
        partitionEnd = int.from_bytes(partition[8:11], "little")
        partitionList.append(
            {
                "type": "{:#03x}".format(partitionType),
                "end": partitionStart + partitionEnd - 1,
                "start": partitionStart,
                "number": i,
            }
        )
    return partitionList


def parse_gpt(gpt_file, sector_size: int = 512) -> list[dict]:
    """parses the gpt and iterates through the table entries and returns the end, name, number, start and type for each entry"""
    partitionList = []
    # the partition start is at byte 72 after the 0th sector
    gpt_file.seek(sector_size + 72)
    partitionStart = int.from_bytes(gpt_file.read(8), "little")
    numEntries = int.from_bytes(gpt_file.read(4), "little")
    entryLength = int.from_bytes(gpt_file.read(4), "little")
    # find the start of the first partition in the file
    gpt_file.seek(sector_size * partitionStart)
    for i in range(numEntries):
        entry = gpt_file.read(entryLength)
        if int.from_bytes(entry[0:16], "little") == 0:
            break
        pType = uuid.UUID(bytes_le=entry[0:16])
        start = int.from_bytes(entry[32:39], "little")
        end = int.from_bytes(entry[40:47], "little")
        name = entry[56:128].decode("utf-16-le").split("\x00", 1)[0]
        partitionList.append({"end": end, "name": name, "number": i, "start": start, "type": pType})
    return partitionList


if __name__ == "__main__":
    with open("test-mbr.dd", "rb") as fd:
        data = fd.read(512)
        parse_mbr(data)

    with open("disk-image.dd", "rb") as fd:
        parse_gpt(fd, 512)
