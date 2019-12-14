import time
import requests
import hashlib
import os
import json
from bs4 import BeautifulSoup

def getHashOfFile(f):
    # Read and update hash string value in blocks of 4K
    readableHash = hashlib.sha256(f).hexdigest()
    return readableHash

class Meme:
    def __init__(self, url, autoDownload=True, soup=None):
        self._soup = soup

        self._title = "UNKNOWN"
        self._id = None
        self._url = url
        self._tags = []
        self._path = "UNKNOWN"
        self._likes = "UNKNOWN"
        self._downloadTime = "UNKNOWN"
        self._imageHash = "UNKNOWN"

        if soup != None:
            self._title = self._getTitleFromSoup()
            self._likes = self._getLikesFromSoup()
            self._id = self._getIdFromSoup()
            self._tags = self._getTagsFromSoup()
        elif autoDownload:
            response = requests.get(url)
            self._soup = BeautifulSoup(response.text, "html.parser")
            self._title = self._getTitleFromSoup()
            self._likes = self._getLikesFromSoup()
            self._id = self._getIdFromSoup()
            self._tags = self._getTagsFromSoup()

    def getDownloadTime(self):
        return self._downloadTime

    def getUrl(self):
        return self._url

    def getTitle(self):
        return self._title
    
    def getLikes(self):
        return self._likes
    
    def getPath(self):
        return self._path
    
    def getId(self):
        return self._id
    
    def getImageHash(self):
        return self._imageHash
    
    def getTags(self):
        return self._tags

    def __repr__(self):
        outS = ""
        outS += "title: " + str(self._title) + "\n"
        outS += "id: " + str(self._id) + "\n"
        outS += "url: " + str(self._url) + "\n"
        outS += "tags: " + str(self._tags)
        outS += "path: " + str(self._path) + "\n"
        outS += "likes: " + str(self._likes) + "\n"
        outS += "downloadTime: " + str(self._downloadTime) + "\n"
        outS += "imageHash: " + str(self._imageHash) + "\n"
        return outS

    def __dict__(self):
        d = {
            "title": self._title,
            "id": self._id,
            "url": self._url,
            "tags": self._tags,
            "path": self._path,
            "likes": self._likes,
            "download_time": self._downloadTime,
            "image_hash": self._imageHash
        }
        return d

    def _getSoup(self):
        if self._soup == None:
            response = requests.get(self._url)
            self._soup = BeautifulSoup(response.text, "html.parser")
        return self._soup

    def _getTitleFromSoup(self):
        soup = self._getSoup()
        article = soup.find("div", {"class":"article-content"})
        title = article.find("h3", {"class": "article-title"}).text
        title = self._filterWhiteSpaces(title)
        return title
    
    def _getLikesFromSoup(self):
        soup = self._getSoup()
        likes = soup.find("vote")[":score"]
        return int(likes)
    
    def _getIdFromSoup(self):
        soup = self._getSoup()
        Id = soup.find("vote")[":id"]
        return int(Id)

    @staticmethod
    def MemeFromArticle(article, autoDownload=True, soup=None):
        url = article.find("a", {"class":"btn-send-messenger facebook-send article-action"})["data-url"]
        return Meme(url, autoDownload=autoDownload, soup=soup)

    @staticmethod
    def _filterWhiteSpaces(s):
        #Filter the spaces before the actual s
        charIndex = 0
        char = s[0]
        while char == ' ' or char=='\n':
            charIndex += 1
            char = s[charIndex]
        s = s[charIndex:]
        #Filter spaces after 
        charIndex = len(s)-1
        char = s[charIndex]
        while char == ' ' or char=='\n':
            charIndex -= 1
            char = s[charIndex]
        s = s[:charIndex+1]
        return s
    
    @staticmethod
    def _saveToFile(image, title, folderPath=""):
        filePath = folderPath + "\\" + title + ".jpg"
        #finds a new name if the one is already taken with a different image
        i = -1
        while os.path.isfile(filePath):
            #check if the files are the same
            i += 1
            filePath = folderPath + "\\" + title + f"({i})" + ".jpg"

        if i > -1:
            filePath = folderPath + "\\" + title + f"({i})" + ".jpg"


        if not os.path.isdir(folderPath):
            os.mkdir(folderPath)

        with open(filePath, "wb") as f:
            f.write(image)
        return filePath

    @staticmethod
    def _filterIllegalchars(title):
        ILLEGAL_CHARS = set(["<", ">", ":", "\"", "/", "\\", "|", "?", "*"])
        for iChar in ILLEGAL_CHARS:
            title = title.replace(iChar, "")
        return title

    def _getTagsFromSoup(self):
        soup = self._getSoup()
        tagsDict = soup.find("tags")[":tags"]
        tagsDict = json.loads(tagsDict)
        tags = []
        for tag in tagsDict:
            tags.append(tag["name"])
        return tags

    def download(self, folderPath):
        """
        Returns true if download successful
        """

        #check if it is a video
        if folderPath[1] != ':':
            folderPath = os.getcwd() + "\\" + folderPath

        soup = self._getSoup()
        classAI = soup.find("div", {"class":"article-image"})
        url = classAI.find("img")["src"]

        image = requests.get(url).content
        self._imageHash = getHashOfFile(image)
        filePath = self._saveToFile(image, self._filterIllegalchars(self._title), folderPath)
        self._path = filePath
        self._downloadTime = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
        return True

if __name__ == "__main__":
    m = Meme("https://jbzd.com.pl/obr/1206370/kontrola-bezpieczenstwa")
    print(m.getTags())
    x = m.__dict__()
    pass
