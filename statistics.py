import csv
import json
import os

import numpy

from downloader import callToFile, syncDownloads
from loadSettings import *
from timeHelper import *


def analyze(settings, call):
    fields = 18
    if settings['plotSubGrid'] == 'true':
        fields = fields * 10

    linksRX = numpy.zeros((fields, fields))
    linksTX = numpy.zeros((fields, fields))

    startTime = getStartTime(settings)
    stopTime = getStopTime(settings)

    monthList = getMonthList(settings)

    shortest = 9999999
    longest = 0
    overallDistance = 0
    links = 0

    snrLowest = 999999
    snrHighest = -999999
    snrAverage = 0; 

    receiverCalls = {}
    senderCalls = {}
    for month in monthList:
        #print('processing: ' + month)
        filterFile = settings['tempDir'] + '/' + callToFile(call) + '_' + month + '.csv'
        with open(filterFile, newline='') as csvfile:
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

                links = links + 1
                distance = int(row[10])
                if distance > longest:
                    longest = distance
                if distance < shortest:
                    shortest = distance

                snr = int(row[4])
                if snr > snrHighest:
                    snrHighest = snr
                if snr < snrLowest:
                    snrLowest = snr
                snrAverage = snrAverage + snr

                overallDistance = overallDistance + distance

                locator = ''
                mode = ''
                if row[6] == call:
                    locator = row[3]
                    mode = 'TX'
                    if row[2] in receiverCalls:
                        receiverCalls[row[2]] += 1
                    else:
                        receiverCalls[row[2]] = 1
                if row[2] == call:
                    locator = row[7]
                    mode = 'RX'
                    if row[6] in receiverCalls:
                        senderCalls[row[6]] += 1
                    else:
                        senderCalls[row[6]] = 1
                if mode == '':
                    raise Exception('problem with filtered csv file. call not consistent! ' + fileName)

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

    print('links in database: ' + str(links))
    print('distance statistics')
    print('  longest  : ' + str(longest))
    print('  shortest : ' + str(shortest))
    print('  overall  : ' + str(overallDistance))
    print('  average  : ' + str(overallDistance/links))
    print('SNR statistics')
    print('  highest  : ' + str(snrHighest))
    print('  lowest   : ' + str(snrLowest))
    print('  average  : ' + str(snrAverage/links))


    locatorGridsTX = 0
    locatorGridsRX = 0
    locatorGridsTXRX = 0
    locatorGridsReached = 0

    for i in range(0,fields):
        for j in range(0,fields):
            if linksRX[i][j] or linksTX[i][j]:
                locatorGridsReached = locatorGridsReached + 1
                if linksRX[i][j] > 0:
                    locatorGridsRX = locatorGridsRX + 1
                if linksTX[i][j] > 0:
                    locatorGridsTX = locatorGridsTX + 1
                if (linksRX[i][j] > 0 ) and (linksTX[i][j] > 0):
                    locatorGridsTXRX = locatorGridsTXRX + 1

    print('grid locator statistics:')
    print('  reached TX or RX  : ' + str(locatorGridsReached))
    print('  reached TX        : ' + str(locatorGridsTX))
    print('  reached RX        : ' + str(locatorGridsRX))
    print('  reached TX and RX : ' + str(locatorGridsTXRX))

    print('stations')
    print('  number of stations which received ' + call + ': ' + str(len(receiverCalls)))
    print('  call and number of connections: ')
    print(receiverCalls)
    print()
    print('  number of stations which were received: ' + str(len(senderCalls)))
    print('  call and number of connections: ')
    print(senderCalls)
    print()
    
# for module testing and downloading without function afterwards:
if __name__ == "__main__":
    settings = loadSettings()
    syncDownloads(settings)
    for call in settings['calls']:
        print('analyzing for call: ' + call)
        analyze(settings, call)
        print()