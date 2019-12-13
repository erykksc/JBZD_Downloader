import pyperclip
from bs4 import BeautifulSoup
import requests
from Meme import Meme

def _getTitleFromArticle(article):
    title = article.find("h3", {"class": "article-title"}).text

    #Filter the spaces before the actual title
    charIndex = 0
    char = title[0]
    while char == ' ' or char=='\n':
        charIndex += 1
        char = title[charIndex]
    title = title[charIndex:]
    #Filter spaces after 
    charIndex = len(title)-1
    char = title[charIndex]
    while char == ' ' or char=='\n':
        charIndex -= 1
        char = title[charIndex]
    title = title[:charIndex+1]
    return title

def _getPhotoFromArticle(article):
    photoUrl = article.find("class", {"class": "article-image"}).find("img")["src"]
    return requests.get(photoUrl)

def _getLikesFromArticle(article):
    pyperclip.copy(str(article))
    likes = article.find("vote")[":score"]
    return likes


response = requests.get("https://jbzd.com.pl/str/1")

soup = BeautifulSoup(response.text, "html.parser")

main = soup.find("main", {"class":"main"})
listening = main.find("section", {"id":"content-container"})

articles = listening.find_all("article", {"class":"article"})

memes = []
for article in articles:
    memes.append(Meme.memeFromArticle(article))

for meme in memes:
    print(meme)
    print()