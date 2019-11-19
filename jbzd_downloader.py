import requests
import sys
import os
from time import gmtime, strftime
from bs4 import BeautifulSoup
import pyperclip

"""
arguments:
-c - copy link\s from clipboard
? - not supported
?-i - infinity number of links
?-f filename - download memes from text file filename
"""

def getTitle(soup):
    titleDiv = soup.find("h3", {"class": "article-title"})
    title = "-".join(titleDiv.find("a").text.split())
    return title

def getImageFromSoup(soup):
    imageDiv = soup.find("div", {"class": "article-image"})
    imageUrl = imageDiv.find("img")["src"]
    image = getImageFromUrl(imageUrl)
    return image

def getImageFromUrl(url):
    response = requests.get(url)
    return response.content

def saveToFile(fileName, image):
    with open("memes/" + fileName + ".jpg", "wb") as f:
        f.write(image)

def doEverythingForUrl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
        
    title = getTitle(soup)
    image = getImageFromSoup(soup)
    if debug:
        print("Saving \"" + title + "\" from" + url)
    saveToFile(title, image)

def getUrlsFromClipboard():
    urls = pyperclip.paste().replace("\r", "").split("\n")
    return urls

def filterUrls(urls):
    """
    returns a list of jbzd/obr urls
    """
    memesUrls = []
    
    for url in urls:
        if url[:24] == "https://jbzd.com.pl/obr/":
            memesUrls.append(url)
    return memesUrls

def main():
    if "-c" in sys.argv:
        urls = getUrlsFromClipboard()
        memesUrls = filterUrls(urls)

        if debug:
            print("Urls:")
            for memeUrl in memesUrls:
                print(memeUrl)

        for memeUrl in memesUrls:
            doEverythingForUrl(memeUrl)
            
if __name__ == "__main__":
    debug = True
    main()
    # link = sys.argv[1]

    # doEverythingForUrl(link)

