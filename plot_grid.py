import matplotlib.pyplot as plt
import numpy
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg
import csv
import json
import os
from timeHelper import *

settings = 'settings.json'
if os.path.isfile('../' + settings):
    settings = '../' + settings
with open(settings) as f:
    settings = json.load(f)


img=mpimg.imread('Maidenhead_Locator_Map.png')
plt.imshow(img)

(ySize, xSize, x) = img.shape

yGrid = ySize/18
xGrid = xSize/18

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
    with open('tmp/' +settings['filter'] + '_' + month + '.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        cnt = 0
        for row in csvreader:
            cnt = cnt + 1
            if cnt == 1:
                continue
            if row[1] < startTime:
                continue
            if row[1] > stopTime:
                continue
                
            locator = ''
            mode = ''
            if row[6] == settings['call']:
                locator = row[3]
                mode = 'TX'
            if row[2] == settings['call']:
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

plt.show()