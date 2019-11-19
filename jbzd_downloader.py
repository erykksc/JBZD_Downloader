import requests
import sys
from bs4 import BeautifulSoup

"""
arguments:
-i - infinity number of links
-f filename - download memes from text file filename
-c - copy link from clipboard
"""

def getTitle(soup):
    titleDiv = soup.find("h3", {"class": "article-title"})
    title = " ".join(titleDiv.find("a").text.split())
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
    with open("memes//"+ fileName + ".jpg", "wb") as f:
        f.write(image)

def doEverythingForLink(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    title = getTitle(soup)
    image = getImageFromSoup(soup)
    saveToFile(title, image)

def getMode():
    if "-i" in sys.argv:
        return ""


if __name__ == "__main__":
    link = sys.argv[1]
    doEverythingForLink(link)

