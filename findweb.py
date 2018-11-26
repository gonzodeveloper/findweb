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
    elif url in visited_sites:
         return False
    else:
        visited_sites.append(url)
        return True


def count_strings(regex, page, recursive=False):
    if validate_url(page) is False:
        return 0
    # try:
    #     response = urlopen(page).read()
    # except (ValueError, HTTPError) as e:
    #     print(e, page)
    #     return 0

    header, response = http_get(page)

    # results = re.findall(regex, str(response), re.IGNORECASE)
    results = re.findall(regex, response, re.IGNORECASE)
    count = 0
    results = 0 if results is None else len(results)

    # print(url)
    if recursive:
        soup = BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser")
        for link in soup:
            print(link)
            if link.has_attr('href'):
                new_link = urljoin(page, link['href'])
                print(new_link)
                count += count_strings(regex, new_link, recursive)
            if link.has_attr('src'):
                print(new_link)
                new_link = urljoin(page, link['src'])
                count += count_strings(regex, new_link, recursive)

    return count + results


if __name__ == "__main__":

    usage = "findweb.py [-r] url regex"

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

    # regex = re.compile(string)
    regex = string.encode()     #I figured regex isn't necessary, byte string is enough
    count = count_strings(regex, page=url, recursive=recursive)
    print()
    print(count)