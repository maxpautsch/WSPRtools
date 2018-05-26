import os
import glob
import urllib.request
import zipfile
import csv
import json
from timeHelper import getMonthList

settings = 'settings.json'
if os.path.isfile('../' + settings):
    settings = '../' + settings
with open(settings) as f:
    settings = json.load(f)

wsprDownloadUrlPrefix = 'http://wsprnet.org/archive/wsprspots-'
wsprDownloadUrlSuffix = '.csv.zip'
# format: Prefix + 2018-05 + Suffix

csvPrefix = 'wsprspots-'
csvSuffix = '.csv'

tmpDir = './tmp'

if settings['cleanDownloads'] == 'true':
    if os.path.isdir(tmpDir):
        files = glob.glob(tmpDir +'/*')
        for f in files:
            os.remove(f)

if not os.path.isdir(tmpDir):
    os.mkdir(tmpDir)

monthList = getMonthList(settings)

for month in monthList:
    print('processing ' + month)

    downloadAs = tmpDir + '/' + month + wsprDownloadUrlSuffix
    csvFile = tmpDir + '/' + csvPrefix + month + csvSuffix 

    if not os.path.isfile(downloadAs):
        print('  downloading')
        url = wsprDownloadUrlPrefix + month + wsprDownloadUrlSuffix
        urllib.request.urlretrieve(url, downloadAs)
    else:
        print('  download skipped. already on disk')
    
    if not os.path.isfile(csvFile):
        print('  extracting')
        with zipfile.ZipFile(downloadAs,"r") as zip_ref:
            zip_ref.extractall(tmpDir)
    else:
        print('  extract skipped. already on disk')

    if settings['cleanup'] == 'true':
        os.remove(downloadAs)

    if settings['filter'] != '':
        print('  analyzing')
        lines = 0

        outFilePath = tmpDir + '/' + settings['filter'] + '_' + month + csvSuffix
        outFile = open(outFilePath,'w')
        outFile.write('spodID,timestamp,,rereporterporterGrid,snr,frequency,call,grid,power,drift,distance,azimuth,band,version,code\n')

        with open(csvFile, 'rU' ) as f:
            lines = 0
            cnt = 0
            for line in f:
                lines = lines +1 
                if settings['call'] in line:
                #print(str(line.encode("utf-8", "surrogateescape")))
                    outFile.write(line)
                    cnt = cnt + 1
            print('  analyzed links: '+str(lines))
            print('  number of links involving ' + settings['call'] +': '+str(cnt))

        if settings['cleanup'] == 'true':
            os.remove(csvFile)

outFile.close()

