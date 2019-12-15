from VaultManager import VaultManager
from Crawler import Crawler
from settingsLoader import loadSettings

if __name__ == "__main__":
    settings = loadSettings("settings.json")
    vault = VaultManager(settings["vault_path"],settings["meme_download_folder_path"], settings["time_between_downloads"], logLevel=0)
    crawler = Crawler(settings["min_likes"], vault, settings["download_memes_images_auto"], settings["meme_download_folder_path"], settings["frequency_of_crawling"], settings["time_between_downloads"], settings["pause_between_page_requests"], settings["page_range"], settings["log_level"])
    crawler.crawlRange()
    vault.fixImagePathsIfWrong()
    vault.downloadMissingImages()