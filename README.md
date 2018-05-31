# WSPRtools
tools to analyze data from wsprnet.org
all settings are don in settings.json
downloader.py downloads all neccessary data and provides one csv per month with filtered call signs.

for plotting install matplotlib: pip3 install matplotlib


source of Maidenhead_Locator_Map.png https://commons.wikimedia.org/wiki/File:Maidenhead_Locator_Map.png (public domain by NASA)
requires python3

## artifacts during analyzis
### download zip file
the zip file is downloaded from http://wsprnet.org/drupal/downloads 
format of url: 'http://wsprnet.org/archive/wsprspots-' + year and month + '.csv.zip'
### extract
extracts to 'wsprspots-' + year and month + '.csv'
### filter
the csv files are filtered. therefore the csv is parsed and if the reporter or the sender is within the call sign list, it is stored in a new csv file. the naming scheme for this is: call + '_' year and month + '.csv'
these files will stay on the disk. the zip file and the extracted csv file will be deleted if the cleanup is set within the settings file
### download startegy
if the filtered file for one call within the call sign list is not present, the zip file for the corresponding month is downloaded if neccessary, and extracted if neccessary.