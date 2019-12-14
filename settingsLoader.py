import json
from colorama import Fore, init

init()

def loadSettings(path, logLevel=3):
    try:
        with open(path,"r") as F:
            loadedF = json.load(F)
            if logLevel==0:
                print(Fore.GREEN +"Settings file loaded correctly" + Fore.RESET)
            return loadedF
    except json.decoder.JSONDecodeError:
        print(Fore.RED + "Settings file damaged" + Fore.RESET)
    except FileNotFoundError:
        if logLevel<=1:
            print(Fore.YELLOW +"No Settings file found, creating a new one" + Fore.RESET)

        newSettings = {
            "pause_between_pageRequests" : 0.5,
            "time_between_downloads" : 0.7,
            "frequency_of_crawling" : 30,
            "meme_download_folder_path" : "",
            "vault_path" : ""
        }
        with open(path,"w") as F:
            json.dump(newSettings , F, indent = 4)
        return loadSettings