# -*- coding: utf-8 -*-
# Author: @eniolw
# License: GNU GPL 3.0

import os
import re
from bs4 import BeautifulSoup
from pprint import pprint


# Put the path to the saved HTML files here:
PATH = ""


def get_distilled_posts_urls(webpages):

    data = []

    for i, html in enumerate(webpages):
        # Create a soup for the webpage:
        try:  
            soup = BeautifulSoup(html.get("content"), "html.parser")

        except:
            print ("Apparently, this HTML file has some errors.")
            continue

        # Select only the content of the post from the webpage:
        post_content = [d
                        for d in soup.find_all("div") 
                        if d.get("class") 
                        and "PostFull__body" in d.get("class")
                       ][0]

        # Select all 'a' elements from the content of the post:
        a_tags = post_content.find_all("a")
        
        # Select only 'a' elements linked to URLs of Steemit posts:
        distilled_a_tags = [l
                            for l in a_tags 
                            if l.get("href") 
                            and re.search("https://steemit.com/.+/@.+/", l.get("href"))
                            and not re.search("@steemstem", l.get("href"))
                           ]

        # Get the pure text of the content of the post:
        post_text = post_content.get_text()

        pattern_base = "handpicked choices.+{}.+A few words about the nomination process"

        # Gather the url and the title of the post if this is a distilled post:
        distilled_data = [{"url": l.get("href"), "title": l.get_text()}
                          for l in distilled_a_tags 
                          if re.search(pattern_base.format(re.escape(l.get_text())), post_text)
                         ]
        # Collect the distilled post data:
        data.extend(distilled_data)

    return data


def load_html_pages(path):
    html_pages = []
    file_names = [a.name for a in os.scandir(path) if a.is_file()]

    for file_name in file_names:
        with open(path + file_name, "r")  as file:
            html_pages.append({
                "name": file_name,
                "content": file.read()
            }) 

    return html_pages


def get_authors_and_tags(data):

    authors = {}
    url_tags = {}

    for post in data:

        author = post.get("url").split("/")[4].replace("@", "")
        tag = post.get("url").split("/")[3]

        if author in authors:
            authors[author] += 1

        else:
            authors[author] = 1

        if tag in url_tags:
            url_tags[tag] += 1

        else:
            url_tags[tag] = 1

    ndata = {
        "authors": sorted([(c, authors[c]) for c in authors], key=lambda x: x[1], reverse=True),
        "tags": sorted([(c, url_tags[c]) for c in url_tags], key=lambda x: x[1], reverse=True)
    }

    return ndata


def main():

    html = load_html_pages(PATH)
    data = get_distilled_posts_urls(html)
    authors_and_tags = get_authors_and_tags(data)

    # pprint(data)
    # pprint(authors_and_tags)
    # Otherwise you can store them to a file


if __name__ == '__main__':
    main()        