import datetime
import time

def getMonthList(settings):
    monthList = []

    if settings['stopNow'] == 'true':
        endYear = datetime.datetime.now().strftime('%Y')
        endMonth = int(datetime.datetime.now().strftime('%m'))

    else:
        endYear = settings['stopYear']
        endMonth = settings['stopMonth']

    if endYear != settings['startYear']:
        raise Exception('not yet implemented: change of year')

    for month in range(int(settings['startMonth']), int(endMonth)+1):
        monthList.append(settings['startYear'] + '-' + str(month).zfill(2))

    return monthList

def getStartTime(settings):
    hour, minute, second = settings['startTime'].split(':')
    return datetime.datetime(int(settings['startYear']),int(settings['startMonth']),int(settings['startDay']),int(hour), int(minute), int(second)).timestamp()

def getStopTime(settings):
    if settings['stopNow'] == 'true':
        return datetime.datetime.now().timestamp()

    else:
        hour, minute, second = settings['stopTime'].split(':')
        return datetime.datetime(int(settings['stopYear']),int(settings['stopMonth']),int(settings['stopDay']),int(hour), int(minute), int(second)).timestamp()
