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

def analyzeGrid(settings,call, band=''):
    
    cnt = 0

    fields = 18
    if settings['plotSubGrid'] == 'true':
        fields = fields * 10

    linksRX = numpy.zeros((fields, fields))
    linksTX = numpy.zeros((fields, fields))

    startTime = getStartTime(settings)
    stopTime = getStopTime(settings)

    monthList = getMonthList(settings)
    for month in monthList:
        print('processing: ' + month)
        if call != '':
            processingFile = settings['tempDir'] + '/' + callToFile(call) + '_' + month + '.csv'
        else:
            processingFile = settings['tempDir'] + '/' + settings['csvSpotsPrefix'] + month + settings['csvSuffix']

        with open(processingFile, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            cnt = 0
            dropReasonLocatorLen = 0
            for row in csvreader:
                cnt = cnt + 1
                if cnt == 1:
                    continue
                if int(row[1]) < startTime:
                    continue
                if int(row[1]) > stopTime:
                    continue

                if band != '' and row[12] != band:
                    continue

                #if len(row[7]) != 6:
                #    dropReasonLocatorLen = dropReasonLocatorLen + 1
                #    continue

                # RX
                if (row[2] == call) or (call == ''):
                    locator = row[7]
                    x = ord(locator[0])-ord('A') 
                    y = 17-(ord(locator[1])-ord('A'))
                    xL = x
                    yL = y
                    #if locator[0] == 'A' and locator[1] == 'D':
                    #    print(row)

                    if settings['plotSubGrid'] == 'true':
                        x = x*10 + ord(locator[2])-ord('0') 
                        y = y*10 + 9 - (ord(locator[3])-ord('0')) 
                    if x>=180 or y>=180:
                        continue
                        print(row)
                        print(locator)
                        print('x: ' + str(x) + ' y: ' + str(y))
                        print('xL: ' + str(xL) + ' yL: ' + str(yL))
                        exit()
                    else:
                        linksRX[x][y] = linksRX[x][y] + 1

                # TX
                if (row[6] == call) or (call == ''):
                    locator = row[3]
                    x = ord(locator[0])-ord('A') 
                    y = 17-(ord(locator[1])-ord('A'))
                    xL = x
                    yL = y

                   # if locator[0] == 'A' and locator[1] == 'D':
                   #     print(row)
                    if settings['plotSubGrid'] == 'true':
                        x = x*10 + ord(locator[2])-ord('0') 
                        y = y*10 + 9 - (ord(locator[3])-ord('0'))    
                    if x>=180 or y>=180:
                        continue
                        print(row)
                        print(locator)
                        print('RXx: ' + str(x) + ' y: ' + str(y))
                        print('xL: ' + str(xL) + ' yL: ' + str(yL))
                        exit()
                    else:
                        linksTX[x][y] = linksTX[x][y] + 1
            print('entries: ' + str(cnt))
            print('drops: ' + str(dropReasonLocatorLen))

    if call == '':
        call = 'world'

    exportTo = settings['gridExportDir'] + '/' + callToFile(call) + '_grid.png'
    if not os.path.isdir(settings['gridExportDir']):
        os.path.mkdirs(settings['gridExportDir'])
    plotGrid(settings, linksTX, linksRX, call, exportTo)




def plotGrid(settings, linksA, linksB, call='', exportTo=''):
    # check if map file is existent. if not: download it
    checkLocatorMap(settings)
    dpi = 300
    img=mpimg.imread(settings['locatorMap'])
    height, width, nbands = img.shape
    figsize = width / float(dpi), height / float(dpi)

    fig = plt.figure(figsize=figsize)
    
    ax = fig.add_axes([0, 0, 1, 1])

    ax.axis('off')
    ax.imshow(img, interpolation='nearest')
    ax.set(xlim=[0, width], ylim=[height, 0], aspect=1)

    fieldsX, fieldsY = linksA.shape

    yGrid = height/fieldsY
    xGrid = width/fieldsX

    for i in range(0,fieldsX):
        for j in range(0,fieldsY):
            if linksA[i][j] or linksB[i][j]:
                colorSet="#FFFFFF"
                if linksA[i][j] > 0:
                    colorSet = '#FF0000'
                if linksB[i][j] > 0:
                    colorSet = '#00FF00'
                if (linksA[i][j] > 0 ) and (linksB[i][j] > 0):
                    colorSet = '#0000FF'
                r = Rectangle([i*xGrid, j*yGrid], xGrid, yGrid, alpha=0.4, color=colorSet) 
                plt.gca().add_artist(r)
    
    patch_tx = mpatches.Patch(color = '#00FF00', label = call + ' TX')
    patch_rx = mpatches.Patch(color = '#FF0000', label = call + ' RX')
    patch_txrx = mpatches.Patch(color = '#0000FF', label = 'TX and RX')
    plt.legend(handles=[patch_tx, patch_rx, patch_txrx])
    #

    if exportTo != '':
        plt.savefig(exportTo, dpi='figure')
    plt.show()


# for module testing and downloading without function afterwards:
if __name__ == "__main__":
    settings = loadSettings()
    syncDownloads(settings)
    for call in settings['calls']:
        analyzeGrid(settings, call)
