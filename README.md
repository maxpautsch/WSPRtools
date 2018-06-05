# WSPRtools
Tools to analyze data from wsprnet.org. Requires python3. 

All settings are done within the file settings.json. Afterwards the analysis can be started.
## Plot grids with links
A map will be downloaded from [wikimedia (public domain by NASA)](https://commons.wikimedia.org/wiki/File:Maidenhead_Locator_Map.png) 
All links are listed in the resulting image. Grids with RX, TX or both are colored.

To plot the grid call: `python3 plotGrid.py`
![grid example](https://github.com/maxpautsch/WSPRtools/raw/master/doc/example_grid.png "grid example")

## Plot complete grids
Plot all grid locator fields with WISPR activity in the configured time

`python3 plotCompleteGrid.py`

## Generate statistics
For generation call: `python3 statistics.py`

![statistics example](https://github.com/maxpautsch/WSPRtools/raw/master/doc/example_statistic.png "statistics example")

# Internals
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
