import csv
import glob
import json
import os
import urllib.request
import zipfile

from loadSettings import *
from timeHelper import *


def callToFile(call):
    call = call.replace('\\','_')
    return call.replace('/','_')

def syncDownloads(settings):
    monthList = getMonthList(settings)

    # make sure, that the target directory exists
    if not os.path.isdir(settings['tempDir']):
        os.mkdir(settings['tempDir'])

    for month in monthList:
        processingMessage = 0
        for call in settings['calls']:
            filterFile = settings['tempDir'] + '/' + callToFile(call) + '_' + month + '.csv'
            if not os.path.isfile(filterFile):
                if processingMessage == 0:
                    print('processing ' + month)
                    processingMessage = 1

                # check if thw raw csv file is there
                csvRawFile = settings['tempDir'] + '/' + settings['csvSpotsPrefix'] + month + settings['csvSuffix']
                if not os.path.isfile(csvRawFile):

                    print('  raw file not existent. need to extract')
                    downloadAs = settings['tempDir'] + '/' + settings['csvSpotsPrefix'] + month + settings['wsprDownloadUrlSuffix']

                    if not os.path.isfile(downloadAs):
                        print('  download is not existend. downloading...')
                        url = settings['wsprDownloadUrlPrefix'] + month + settings['wsprDownloadUrlSuffix']
                        urllib.request.urlretrieve(url, downloadAs)

                    print('  unzip')
                    with zipfile.ZipFile(downloadAs,"r") as zip_ref:
                        zip_ref.extractall(settings['tempDir'])

                outFile = open(filterFile,'w')
                outFile.write('spotID,timestamp,reporter,reporterGrid,snr,frequency,call,grid,power,drift,distance,azimuth,band,version,code\n')
                #              0      1         2        3            4   5         6    7    8     9     10       11      12   13      14
                print('  extracting ' + call)

                cnt = 0
                foundCnt = 0

                callSearch = ',' + call + ','

                with open(csvRawFile, 'rU' ) as f:
                    for line in f:
                        if callSearch in line:
                            outFile.write(line)
                            foundCnt = foundCnt + 1
                        cnt = cnt + 1
                outFile.close()

                print('  analyzed links: '+str(cnt))
                print('  number of links involving ' + call +': '+str(foundCnt))

        if settings['cleanup'] == 'true':
            # remove unfiltered csv file
            csvRawFile = settings['tempDir'] + '/' + settings['csvSpotsPrefix'] + month + settings['csvSuffix']
            if os.path.isfile(csvRawFile):
                os.remove(csvRawFile)
            # remove zip file
            downloadAs = settings['tempDir'] + '/' + settings['csvSpotsPrefix'] + month + settings['wsprDownloadUrlSuffix']
            if os.path.isfile(downloadAs):
                os.remove(downloadAs)


# for module testing and downloading without function afterwards:
if __name__ == "__main__":
    print('checking for needed downloads and extracting for calls...')
    syncDownloads(loadSettings())




