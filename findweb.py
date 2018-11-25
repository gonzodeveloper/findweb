#!/bin/python3
#
# Description: Script that takes in command line arguments to search a url for a given string
# Authors: Kyle Hart, Sayera Dhaubhadel

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, SoupStrainer
import re
import sys
import socket


visited_sites = []


def validate_url(url):
    parsed = urlparse(url)

    if parsed.scheme not in ['http', ''] or url in visited_sites:
        return False
    else:
        visited_sites.append(url)
        return True


def count_strings(regex, page, recursive=False):
    if validate_url(page) is False:
        return 0
    try:
        response = urlopen(page).read()
    except (ValueError, HTTPError) as e:
        print(e, page)
        return 0

    results = re.findall(regex, str(response))

    count = 0
    results = 0 if results is None else len(results)

    print(url)
    if recursive:
        soup = BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser")
        for link in soup:
            print("\t", link)
            if link.has_attr('href'):
                new_link = urljoin(page, link['href'])
                count += count_strings(regex, new_link, recursive)
            if link.has_attr('src'):
                new_link = urljoin(page, link['src'])
                count += count_strings(regex, new_link, recursive)

    return count + results


def http_get(url):
    regex = r"^(?:(?:http[s]?|ftp):\/)?\/?([^:\/\s]+)((?:(?:\/\w+)*\/)(?:[\w\-\.]+[^#?\s]+)(?:.*)?(?:#[\w\-]+)?)$"
    url_split = re.findall(regex, url)
    host = url_split[0]
    path = url_split[1]
    request_query = b"GET {} HTTP/1.1\r\nHost:{}\r\nUser-Agent: \r\nAccept:*/*\r\n\r\n".format(host, path)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_ip = socket.gethostbyname(url)
    port = 80
    BUFFER_LENGTH = 400
    data = b''

    s.connect((host_ip, port))
    s.send(request_query)

    while (True):
        packet = s.recv(BUFFER_LENGTH)
        data += packet
        print(1)
        if len(packet) < BUFFER_LENGTH:
            break
    print(data)
    header, data = data.split(b'\r\n\r\n', 2)
    print('header :', header)
    print('data :', data)
    header_split = header.split(b'\r\n')
    print('header split: ', len(header_split), header_split)

if __name__ == "__main__":

    usage = "findweb [-r] url regex"

    if len(sys.argv) > 4:
        print(usage)
        exit(1)

    if sys.argv[1] == "-r":
        recursive = True
        url = sys.argv[2]
        string = sys.argv[3]
    else:
        recursive = False
        url = sys.argv[1]
        string = sys.argv[2]

    regex = re.compile(string)
    count = count_strings(regex, page=url, recursive=recursive)
    print(count)