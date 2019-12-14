import os
import sys
import json
import time
from Meme import Meme, getHashOfFile
from colorama import Fore, init

init()

def _getTime():
    t = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    return t

class VaultManager:
    def __init__(self, vaultFilePath, memeDownloadFolderPath, timeBetweenDownloads=0.7, logLevel=2):
        #log levels
        #0 - debug
        #1 - warning
        #2 - critical error
        #3 - none
        self._vaultFilePath = vaultFilePath
        self._logLevel = logLevel
        self._vault = self._loadVault()
        self._memeDownloadFolderPath = memeDownloadFolderPath
        self._timeBetweenDownloads = timeBetweenDownloads
        

    @staticmethod
    def _getNewDictVault():
        rJson = {
            "database_creation_time" : _getTime(),
            "last_modification_time" : _getTime(),
            "memes" : []
        }
        return rJson
    
    def _saveVault(self):
        self._vault["last_modification_time"] = _getTime()
        with open(self._vaultFilePath,"w") as F:
            json.dump(self._vault , F, indent = 4)
        if self._logLevel == 0:
            print(f"{Fore.GREEN}Vault file saved{Fore.RESET}")

    def _loadVault(self):
        """Loads vault from a file vaultFilePath.json"""
        try:
            with open(self._vaultFilePath, "r") as F:
                loadedF = json.load(F)
                if self._logLevel == 0:
                    print(Fore.GREEN +"Vault file loaded correctly" + Fore.RESET)
                return loadedF
        except json.decoder.JSONDecodeError:
            print(Fore.RED + "Vault file damaged" + Fore.RESET)
        except FileNotFoundError:
            if self._logLevel<=1:
                print(Fore.YELLOW +"No vault file found, creating a new one" + Fore.RESET)
            with open(self._vaultFilePath,"w") as F:
                json.dump(self._getNewDictVault() , F, indent = 4)
            return self._loadVault()
    
    def _getMemeVaultIndex(self, meme:Meme):
        #if it returns -1, it means the meme is not in vault
        for i, vMeme in enumerate(self._vault["memes"]):
            if vMeme["id"] == meme.getId():
                return i
        return -1

    def _isMemeInVault(self, meme:Meme):
        memeIndex = self._getMemeVaultIndex(meme)
        if memeIndex !=-1:
            return True
        else:
            return False

    def isMemeDownloaded(self, meme:Meme):
        memeIndex = self._getMemeVaultIndex(meme)
        if memeIndex == -1:
            return False
        else:
            vMeme = self._vault["memes"][memeIndex]
            if (vMeme["path"] == "UNKNOWN") or (vMeme["path"] == "MISSING"):
                return False
            else:
                return True
    
    def _isVaultMemeUpdated(self, meme:Meme):
        memeIndex = self._getMemeVaultIndex(meme)
        if memeIndex == -1:
            return False
        else:
            vMeme = self._vault["memes"][memeIndex]
            for key in meme.__dict__().keys():
                if vMeme[key] != meme.__dict__()[key]:
                    if meme.__dict__()[key] != "UNKNOWN":
                        return False
            return True
    
    def _getNotMatchingKeysWithVault(self, meme:Meme):
        memeIndex = self._getMemeVaultIndex(meme)
        if memeIndex == -1:
            return False
        else:
            rKeys = []
            vMeme = self._vault["memes"][memeIndex]
            for key in meme.__dict__().keys():
                if vMeme[key] != meme.__dict__()[key]:
                    if meme.__dict__()[key] != "UNKNOWN":
                        rKeys.append(key)
            return rKeys
    
    def fixImagePathsIfWrong(self):
        for i, meme in enumerate(self._vault["memes"]):
            path = meme["path"]
            memeId = meme["id"]
            if path != "UNKNOWN":
                if os.path.isfile(path):
                    with open(path, "rb") as f:
                        image = f.read()
                    if getHashOfFile(image) != meme["image_hash"]:
                        self._vault["memes"][i]["path"] = "MISSING"
                        modTime = _getTime()
                        self._vault["memes"][i]["last_path_validity_check"] = modTime
                        self._vault["memes"][i]["last_database_modification"] = modTime
                        if self._logLevel == 0:
                            print(Fore.YELLOW + f"Meme's {memeId} image doesn't exist" + Fore.RESET)
                else:
                    self._vault["memes"][i]["path"] = "MISSING"
                    modTime = _getTime()
                    self._vault["memes"][i]["last_path_validity_check"] = modTime
                    self._vault["memes"][i]["last_database_modification"] = modTime
                    if self._logLevel == 0:
                        print(Fore.YELLOW + f"Meme's {memeId} image doesn't exist" + Fore.RESET)
        self._saveVault()
    
    def downloadMissingImages(self, paths2Download=["MISSING", "UNKNOWN"]):
        # paths2Download can ben for example ["MISSING", "UNKNOWN"]
        for i, meme in enumerate(self._vault["memes"]):
            path = meme["path"]
            memeId = meme["id"]
            if path in paths2Download:
                myMeme = Meme(meme["url"])
                try:
                    myMeme.download(self._memeDownloadFolderPath)
                    self._vault["memes"][i]["path"] = myMeme.getPath()
                    self.addMemeToVault(myMeme, addedBy=meme["added_by"])
                    time.sleep(self._timeBetweenDownloads)
                    if self._logLevel == 0:
                        print(Fore.GREEN + f"Missing meme {myMeme.getId()} ({myMeme.getTitle()}) image has been downloaded to {myMeme.getPath()}" + Fore.RESET)
                except:
                    if self._logLevel==0:
                        print(f"{Fore.RED}Meme {myMeme.getId()} ({myMeme.getTitle()}) download failed, possibly a video{Fore.RESET}")
                
        self._saveVault()

    def addMemeToVault(self, meme:Meme, addedBy="auto", save=True):
        if self._isMemeInVault(meme) == False:
            memeDict = meme.__dict__()
            memeDict["last_path_validity_check"] = "Unknown"
            memeDict["last_likes_check_time"] = _getTime()
            memeDict["last_database_modification"] = _getTime()
            memeDict["added_by"] = addedBy
            
            if self._logLevel == 0:
                print(f"Adding meme {meme.getId()} ({meme.getTitle()}) to vault")

            self._vault["memes"].append(memeDict)
            if save:
                self._saveVault()
            return True

        elif not self._isVaultMemeUpdated(meme):
            memeDict = meme.__dict__()
                   
            memeIndex = self._getMemeVaultIndex(meme)
            for key in self._getNotMatchingKeysWithVault(meme):
                self._vault["memes"][memeIndex][key] = memeDict[key]
                if self._logLevel == 0:
                    print(f"Updating meme {meme.getId()} ({meme.getTitle()}) key {key} in vault to {memeDict[key]}")
                if key == "path":
                    self._vault["memes"][memeIndex]["last_path_validity_check"] = _getTime()

            self._vault["memes"][memeIndex]["last_database_modification"] = _getTime()
            self._vault["memes"][memeIndex]["last_likes_check_time"] = _getTime()

            if save:
                self._saveVault()
            return True

        else:
            if self._logLevel == 0:
                print(Fore.MAGENTA + f"Meme {meme.getId()} ({meme.getTitle()}) is already in Vault" + Fore.RESET)
            return False
        
    def addMemeBatchToVault(self, memeBatch, addedBy="auto"):
        anythingSaved = False
        for meme in memeBatch:
            flag = self.addMemeToVault(meme, addedBy=addedBy, save=False)
            if flag:
                anythingSaved = True
        if anythingSaved:
            self._saveVault()