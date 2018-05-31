import json
import os
import re

settingsFile = 'settings.json'

def loadSettings():
    global settingsFile

    # check, if there is a private version of the settings file
    # (to hide call signs in the repo ;) )
    if os.path.isfile('../' + settingsFile):
        settingsFile = '../' + settingsFile

    with open(settingsFile, 'r') as f:
        data = f.read()
        data = re.sub(r'\\\n', '', data)
        data = re.sub(r'//.*\n', '\n', data)
        settings = json.loads(data)
        return settings

# for module testing:
if __name__ == "__main__":
    print('settings in file:')
    print(loadSettings())