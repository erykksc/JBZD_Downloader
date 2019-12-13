import time
import requests
import hashlib
import os
from bs4 import BeautifulSoup

import pyperclip
class Meme:
    def __init__(self, url, autoDownload=True):
        self._soup = None

        self._downloadTime = "UNKNOWN"
        self._lastVCT = "UNKNOWN" #last validity check time
        self._lastLCT = "UNKNOWN" #last likes check time
        self._url = url
        self._title = "UNKNOWN"
        self._path = "UNKNOWN"
        self._likes = "UNKNOWN"
        self._id = None
        self._imageHash = "UNKNOWN"

        if autoDownload:
            response = requests.get(url)
            self._soup = BeautifulSoup(response.text, "html.parser")
            self._title = self._getTitleFromSoup()
            self._likes = self._getLikesFromSoup()
            self._id = self._getIdFromSoup()

    def getDownloadTime(self):
        return self._downloadTime
    
    def getLastVCT(self):
        return self._lastVCT
    
    def getLastLCT(self):
        return self._lastLCT

    def getUrl(self):
        return self._url

    def getTitle(self):
        return self._title
    
    def getLikes(self):
        return self._likes
    
    def getPath(self):
        return self._path

    def __repr__(self):
        outS = ""
        outS += "title:" + str(self._title) + "\n"
        outS += "Id:" + str(self._id) + "\n"
        outS += "url:" + str(self._url) + "\n"
        outS += "path:" + str(self._path) + "\n"
        outS += "likes:" + str(self._likes) + "\n"
        outS += "downloadTime:" + str(self._downloadTime) + "\n"
        outS += "lastVCT:" + str(self._lastVCT) + "\n"
        outS += "lastLCT:" + str(self._lastLCT)
        return outS

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
    def memeFromArticle(article, autoDownload=True):
        pyperclip.copy(str(article))
        url = article.find("a", {"class":"btn-send-messenger facebook-send article-action"})["data-url"]
        return Meme(url, autoDownload=autoDownload)

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
        filePath = folderPath + title + ".jpg"
        #finds a new name if the one is already taken with a different image
        i = -1
        while os.path.isfile(filePath):
            #check if the files are the same
            i += 1
            filePath = folderPath + title + f"({i})" + ".jpg"

        if i > -1:
            filePath = folderPath + title + f"({i})" + ".jpg"


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
        
    @staticmethod
    def _getHashOfFile(f):
        # Read and update hash string value in blocks of 4K
        readableHash = hashlib.sha256(f).hexdigest()
        return readableHash

    def download(self, folderPath):
        """
        Returns true if download successful
        """
        if folderPath == "":
            folderPath = os.getcwd() + "\\"
        soup = self._getSoup()
        classAI = soup.find("div", {"class":"article-image"})
        url = classAI.find("img")["src"]

        image = requests.get(url).content
        self._imageHash = self._getHashOfFile(image)
        filePath = self._saveToFile(image, self._filterIllegalchars(self._title), folderPath)
        self._path = filePath
        self._downloadTime = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
        return True

if __name__ == "__main__":
    m = Meme("https://jbzd.com.pl/obr/1206192/ze-co")
    m.download("")
    print(m)
