from plotGrid import *
from downloader import callToFile, syncDownloads
from loadSettings import *


# this file is here for convinience ;)
# it plots ALL TX and RX grids without call filtering
if __name__ == "__main__":
    settings = loadSettings()
    syncDownloads(settings)
    analyzeGrid(settings, '', '7')