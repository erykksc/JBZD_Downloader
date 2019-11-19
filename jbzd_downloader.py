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
    cwd = os.getcwd()
    filePath = os.path.join(cwd, "Memes", fileName) + ".jpg"
    #finds a new name if the one is already taken with a different image
    i = -1
    while os.path.isfile(filePath):
        #check if the files are the same
        with open(filePath, "rb") as f:
            if image == f.read():
                if debug:
                    if i == -1:
                        print(f"File {fileName}.jpg already exists")
                    else:
                        print(f"File already exists and is called {fileName}({i}).jpg")
                return False
            else:
                i += 1
                filePath = os.path.join(cwd, "Memes", fileName + "(" + str(i)) + ").jpg"
    if i > -1:
        fileName = fileName + "(" + str(i) + ")"
    
    if not os.path.isdir(os.path.join(cwd, "Memes")):
        if debug:
            print("NO FOLDER \"Memes FOUND\". CREATING FOLDER \"Memes\"")
        os.mkdir(os.path.join(cwd, "Memes"))

    with open("Memes/" + fileName + ".jpg", "wb") as f:
        f.write(image)
    return True


def doEverythingForUrl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
        
    title = getTitle(soup)
    image = getImageFromSoup(soup)
    if debug:
        if saveToFile(title, image):
            print("Saved \"" + title + "\" from " + url)

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
        if len(memesUrls) == 0:
            print("No valid urls in clipboard")
        else:
            if debug:
                print("Urls:")
                for memeUrl in memesUrls:
                    print(memeUrl)
                print()

        for memeUrl in memesUrls:
            doEverythingForUrl(memeUrl)
            
if __name__ == "__main__":
    debug = True
    main()
    # link = sys.argv[1]

    # doEverythingForUrl(link)

