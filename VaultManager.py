import os
import sys
import json

class VaultManager:
    def __init__(self, vaultFilePath, logLevel=):
        #log levels
        #0 - debug
        #1 - warning
        #2 - critical error
        #3 - none
        self._vault = _loadVault(vaultFilePath)

    def _loadVault(vaultFilePath):
	"""Loads settings from a file vaultFilePath.json"""
	try:
		with open(vaultFilePath,"r") as F:
			return json.load(F)
	except FileNotFoundError:
		with open("SketchRegSettings.json","w") as F:
			json.dump(newSettings , F, indent = 4)
		return loadSettings()

    def _getNewDictVault(self):
        rJson = {
            "Creation time" : "TIME_PLACEHOLDER",
            "Modification time" : "TIME_PLACEHOLDER"
        }
