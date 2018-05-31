import csv
import json
import os
import urllib.request

import matplotlib.image as mpimg
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy
from matplotlib.patches import Rectangle

from downloader import callToFile, syncDownloads
from loadSettings import *
from timeHelper import *


def checkLocatorMap(settings):
    if not os.path.isfile(settings['locatorMap']):
        print('downloading locator map from: ' + settings['locatorMapURL'])
        urllib.request.urlretrieve(settings['locatorMapURL'], settings['locatorMap'])

def plotGrid(settings, call):
    # check if map file is existent. if not: download it
    checkLocatorMap(settings)
    dpi = 300
    img=mpimg.imread('Maidenhead_Locator_Map.png')
    height, width, nbands = img.shape
    figsize = width / float(dpi), height / float(dpi)

    fig = plt.figure(figsize=figsize)
    
    ax = fig.add_axes([0, 0, 1, 1])

    ax.axis('off')
    ax.imshow(img, interpolation='nearest')
    ax.set(xlim=[0, width], ylim=[height, 0], aspect=1)

    yGrid = height/18
    xGrid = width/18

    fields = 18
    if settings['plotSubGrid'] == 'true':
        yGrid = yGrid / 10
        xGrid = xGrid / 10
        fields = fields * 10


    linksRX = numpy.zeros((fields, fields))
    linksTX = numpy.zeros((fields, fields))

    startTime = getStartTime(settings)
    stopTime = getStopTime(settings)

    monthList = getMonthList(settings)
    for month in monthList:
        print('processing: ' + month)
        with open('tmp/' + callToFile(call) + '_' + month + '.csv', newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            cnt = 0
            for row in csvreader:
                cnt = cnt + 1
                if cnt == 1:
                    continue
                if int(row[1]) < startTime:
                    continue
                if int(row[1]) > stopTime:
                    continue

                locator = ''
                mode = ''
                if row[6] == call:
                    locator = row[3]
                    mode = 'TX'
                if row[2] == call:
                    locator = row[7]
                    mode = 'RX'

                if mode != '':
                    x = ord(locator[0])-ord('A') 
                    y = 17-(ord(locator[1])-ord('A'))

                    if settings['plotSubGrid'] == 'true':
                        x = x*10 + ord(locator[2])-ord('0') 
                        y = y*10 + 9 - (ord(locator[3])-ord('0')) 

                    if mode == 'TX':
                        linksTX[x][y] = linksTX[x][y] + 1
                    else:
                        linksRX[x][y] = linksRX[x][y] + 1



    for i in range(0,fields):
        for j in range(0,fields):
            if linksRX[i][j] or linksTX[i][j]:
                colorSet="#FFFFFF"
                if linksRX[i][j] > 0:
                    colorSet = '#FF0000'
                if linksTX[i][j] > 0:
                    colorSet = '#00FF00'
                if (linksRX[i][j] > 0 ) and (linksTX[i][j] > 0):
                    colorSet = '#0000FF'
                r = Rectangle([i*xGrid, j*yGrid], xGrid, yGrid, alpha=0.4, color=colorSet) 
                plt.gca().add_artist(r)
    
    patch_tx = mpatches.Patch(color = '#00FF00', label = call + ' TX')
    patch_rx = mpatches.Patch(color = '#FF0000', label = call + ' RX')
    patch_txrx = mpatches.Patch(color = '#0000FF', label = 'TX and RX')
    plt.legend(handles=[patch_tx, patch_rx, patch_txrx])
    #

    if not os.path.isdir(settings['gridExportDir']):
        os.mkdir(settings['gridExportDir'])

    plt.savefig(settings['gridExportDir'] + '/' + callToFile(call) + '_grid.png', dpi='figure')
    plt.show()


# for module testing and downloading without function afterwards:
if __name__ == "__main__":
    settings = loadSettings()
    syncDownloads(settings)
    for call in settings['calls']:
        plotGrid(settings, call)
