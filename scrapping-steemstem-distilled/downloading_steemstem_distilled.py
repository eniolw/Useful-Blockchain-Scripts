# -*- coding: utf-8 -*-
# Author: @eniolw
# License: GNU GPL 3.0

import requests
import time
from bs4 import BeautifulSoup


# Put the path to the saved HTML files here:
PATH = ""


def download_html_pages(urls):

    html_pages = []
    error = []

    for i, url in enumerate(urls):
        print ("{0}/{1}".format(i + 1, len(urls)))

        time.sleep(1)

        try:
            web = requests.get(url)

        except:
            print ("Error with request on ", url)
            error.append(url)
            continue

        try:
            soup = BeautifulSoup(web.content, "html.parser")

        except:
            print ("Error the HTML content on ", url)
            error.append(url)
            continue

        if not '<div class="PostFull__body' in str(web.content):
            print ("Error: empty page: ", url)
            error.append(url)
            continue      

        print ("Nice")

        html_pages.append({
            "url": url,
            "content": web.content
        })
        with open(PATH + url.split("/")[5], "w")  as file:
            file.write(str(web.content))

    return html_pages, error


def main():

    # We set the URLs of the webpages to be downloaded:
    url_base = "https://steemit.com/steemstem/@steemstem/steemstem-distilled-{0}"
    urls = [url_base.format(i) for i in range(1, 90 + 1)]

    # I already figured out that the following URLs were missing:
    """urls = [
        "https://steemit.com/steemstem/@steemstem/steemstem-distilled-5x13"
        "https://steemit.com/steemstem/@steemstem/introducing-steemstem-distilled-4"
        "https://steemit.com/steemstem/@steemstem/introducing-steemstem-distilled-1",
    ]"""

    # Downloading and storing this webpages:
    html_pages, error_urls = download_html_pages(urls)


if __name__ == '__main__':
    main()        