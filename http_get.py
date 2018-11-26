import sys
import socket


def http_get(url):
    regex = r"^(?:(?:http[s]?|ftp):\/)?\/?([^:\/\s]+)((?:(?:\/\w+)*\/)(?:[\w\-\.]+[^#?\s]+)?(?:.*)?(?:#[\w\-]+)?)?$"
    # regex = r"^(?:(?:http[s]?|ftp):\/)?\/?(?:[^:\/\s]+)(?:(?:(?:\/\w+)*\/)(?:[\w\-\.]+[^#?\s]+)?(?:.*)?(?:#[\w\-]+)?)?$"

    url_split = re.findall(regex, url, re.IGNORECASE)
    print("url split ", url_split)
    url_split = list(url_split[0])

    if(url_split[1] == ""):
        url_split[1] = "/"
    host = url_split[0]
    path = url_split[1]
    request_query = "GET {} HTTP/1.1\r\nHost:{}\r\nUser-Agent: \r\nAccept:*/*\r\n\r\n".format(path, host).encode()
    print(request_query)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)

    port = 80
    BUFFER_LENGTH = 400
    data = b''

    s.connect((host, port))
    s.send(request_query)

    while (True):
        try:
            packet = s.recv(BUFFER_LENGTH)
            data += packet
            # if len(packet) < BUFFER_LENGTH:
            #     break
        except socket.timeout:
            break

    header, data = data.split(b'\r\n\r\n', maxsplit=1)
    print('header :', header)
    print('data :', data)
    header_split = header.split(b'\r\n')
    print('header split: ', len(header_split), header_split)

    for hdr in header_split:
        if hdr.startswith(b"Content-Type:"):
            key, value = hdr.split(b": ")
            if value.startswith(b"text/html"):
                pass
            else:
                print("Content type isn't what is desired")
                exit()
    return header, data


if __name__ == "__main__":
    url = sys.argv[1]
    page = http_get(url)

    print(page)