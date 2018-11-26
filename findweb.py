#!/bin/python3
#
# Description: Script that takes in command line arguments to search a url for a given string
# Authors: Kyle Hart, Sayera Dhaubhadel

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, SoupStrainer
from pathlib import Path
import re
import sys


visited_sites = []


def validate_url(url, parent):
    parsed_url = urlparse(url)
    parsed_parent = urlparse(parent)

    child_path  = Path(parsed_url.path)
    parent_path = Path(parsed_parent.path)

    if parsed_url.scheme not in ['http', ''] \
            or url in visited_sites \
            or parent_path not in child_path.parents:
        return False
    else:
        visited_sites.append(url)
        return True


def count_strings(regex, page_url, recursive=False, depth=0):

    try:
        response = urlopen(page_url).read()
    except (ValueError, HTTPError) as e:
        print(e, page_url)
        return 0

    # header, response = http_get(page)

    results = re.findall(regex, str(response))

    count = 0
    results = 0 if results is None else len(results)
    print("\t" * depth, page_url, " : \t", results)

    if recursive:
        soup = BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser")
        for link in soup:
            if link.has_attr('href'):
                new_link = urljoin(page_url, link['href'])
                if validate_url(new_link, page_url):
                    count += count_strings(regex, new_link, recursive, depth + 1)
            if link.has_attr('src'):
                new_link = urljoin(page_url, link['src'])
                if validate_url(new_link, page):
                    count += count_strings(regex, new_link, recursive, depth + 1)

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

    regex = re.compile(string)
    count = count_strings(regex, page_url=url, recursive=recursive)
    print()
    print("Total hits: ", count)