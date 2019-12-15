from bs4 import BeautifulSoup
import requests
from Meme import Meme
from VaultManager import VaultManager
from colorama import Fore, init
import time

init()

class Crawler:
    def __init__(self, minLikes, vault:VaultManager, download=False, downloadFolderPath="", crawlingFrequency=30, timeBetweenDownloads=0.7, timeBetweenPageRequests=0.5, pageRange=(1, 10), logLevel=2):
        self._minLikes = minLikes
        self._pageRange = pageRange
        self._vaultManager = vault
        self._download = download
        self._downloadFolderPath = downloadFolderPath
        self._crawlingFrequency = crawlingFrequency
        self._timeBetweenDownloads = timeBetweenDownloads
        self._timeBetweenPageRequests = timeBetweenPageRequests
        self._logLevel = logLevel
    

    def crawlRange(self):
        for i in range(self._pageRange[0], self._pageRange[1]+1):
            if self._logLevel==0:
                print(f"Crawling page number: {i}")
            self.checkPage(i)
            time.sleep(self._timeBetweenPageRequests)
    
    def crawlStart(self):
        while True:
            for i in range(self._pageRange[0], self._pageRange[1]+1):
                if self._logLevel==0:
                    print(f"Crawling page number: {i}")
                self.checkPage(i)
                time.sleep(self._timeBetweenPageRequests)
            time.sleep(self._crawlingFrequency)

    def getMinLikes(self):
        return self._minLikes
    
    def checkPage(self, pageNum):
        response = requests.get("https://jbzd.com.pl/str/" + str(pageNum))
        soup = BeautifulSoup(response.text, "html.parser")

        main = soup.find("main", {"class":"main"})
        listening = main.find("section", {"id":"content-container"})

        articles = listening.find_all("article", {"class":"article"})

        memes2Add = []
        for article in articles:
            candidate = Meme.MemeFromArticle(article)
            if "video" not in candidate.getTags():
                if candidate.getLikes() >= self._minLikes:
                    if self._logLevel==0:
                        print(f"Candidate meme {candidate.getId()} ({candidate.getTitle()}) has enough likes {candidate.getLikes()}/{self._minLikes} and is not a video")
                    memes2Add.append(candidate)

        for meme in memes2Add:
            if self._download:
                if not self._vaultManager.isMemeDownloaded(meme):
                    if self._logLevel==0:
                        print(f"{Fore.CYAN}Downloading meme {meme.getId()} ({meme.getTitle()}) to {self._downloadFolderPath}{Fore.RESET}")
                    try:
                        meme.download(self._downloadFolderPath)
                    except:
                        if self._logLevel==0:
                            print(f"{Fore.RED}Meme {meme.getId()} ({meme.getTitle()}) download failed, possibly a video")
                    time.sleep(self._timeBetweenDownloads)
                    if self._logLevel==0:
                        print(f"{Fore.GREEN}Meme {meme.getId()} ({meme.getTitle()}) downloaded to {meme.getPath()}{Fore.RESET}")
        self._vaultManager.addMemeBatchToVault(memes2Add, addedBy="Crawler V1.0")