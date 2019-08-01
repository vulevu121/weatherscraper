# Written by Vu Le
# Spring 2018
# Prof. Glenn Healey

import csv
import time
import math
import json
from parse_h import conv2utc, getAirDensity, getClosestMeas
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, tzinfo

def parse(pitchesfilename, stationNum=1, startRow=0):
    start = time.time()

    ##pitchesfilename = 'WeatherCompTableRev_vu_part1_parsed_parsed.csv'
    ##startRow = 0
    ##stationNum = 3

    with open('ballparks.json', 'r') as f:
        bpdata = json.load(f)

    print('Parsing file...')
    with open(pitchesfilename, mode='r', newline='') as ifile:
        reader = csv.DictReader(ifile)
        fieldnames = reader.fieldnames

        if stationNum == 1:
            fieldnames.append('offset')
        fieldnames.append('station{}code'.format(stationNum))
        #fieldnames.append('t{}diff'.format(stationNum))
        fieldnames.append('station{}dist'.format(stationNum))
        fieldnames.append('temp{}'.format(stationNum))
        fieldnames.append('t{}difftemp'.format(stationNum))
        fieldnames.append('rh{}'.format(stationNum))
        fieldnames.append('t{}diffrh'.format(stationNum))
        fieldnames.append('pres{}'.format(stationNum))
        fieldnames.append('t{}diffpres'.format(stationNum))
        fieldnames.append('airdensity{}'.format(stationNum))

        if startRow > 0:
            permission = 'a'
        else:
            permission = 'w'
        
        with open('{}_parsed.csv'.format(pitchesfilename[0:-4]), mode=permission, newline='') as ofile:
            writer = csv.DictWriter(ofile, fieldnames=fieldnames)
            if startRow == 0:
                writer.writeheader()
            
            lastgameName = 'none'
            gameName = ''

            percent = 1

            row_count = 704367
            row_mod = row_count // 100

            for row in reader:
                if reader.line_num % row_mod == 0:
                    print('Progress: {}% / Line: {}'.format(percent, reader.line_num, (time.time() - start)))
                    percent += 1
     
                if reader.line_num >= startRow:
                    gameName = row['gameName']
                    sv_id = row['sv_id']
                    venue = row['venue']
                    forecast = row['forecast']
                    csvtemp = float(row['temperature'])
                    starttime = row['Time']
                    time_zone = row['time_zone']
                    altitude = float(row['Altitude'])
                    gameLength = row['gameLength']
                    ampm = row['ampm']
                    
                    gameNameSplit = gameName.split(sep='_')
                    gameLengthSplit = gameLength.split(sep=':')

                    year = gameNameSplit[1]
                    month = gameNameSplit[2]
                    day = gameNameSplit[3]

                    if sv_id[-2:] == '60':
                        sv_id = '{}59'.format(sv_id[0:-2])
                    row['sv_id'] = sv_id
                    
                    dtsv_id = datetime.strptime('{} UTC+0000'.format(sv_id), '%y%m%d_%H%M%S %Z%z')
                    dtGameLength = timedelta(hours=int(gameLengthSplit[0]),
                                             minutes=int(gameLengthSplit[1]))
                    
                    dtStartTime = datetime.strptime('{}{}{}{}{}UTC-0400'.format(year, month, day, starttime, ampm), '%Y%m%d%I:%M:%S%p%Z%z')

                    dtStartTime_GameLength = dtStartTime + dtGameLength

                    if stationNum == 1:
                        offset = '0.00'
                        if (dtsv_id < dtStartTime):
                            timediff = abs(dtStartTime - dtsv_id)
                            offset = '-{:0.2f}'.format(timediff.total_seconds()/60)
                        elif (dtsv_id >= dtStartTime) and (dtsv_id <= dtStartTime_GameLength):
                            offset = '0.00';
                        elif (dtsv_id > dtStartTime_GameLength):
                            timediff = abs(dtsv_id - dtStartTime_GameLength)
                            offset = '{:0.2f}'.format(timediff.total_seconds()/60)

                        row['offset'] = offset

                    if gameName != lastgameName:
                        code = bpdata[venue]['closest_ap{}_code'.format(stationNum)]
                        
                        htmlfilename = 'wunderground/{}_{}_{}_{}.html'.format(year, month, day, code)

      
                        with open(htmlfilename) as htmlfile:
                            soup = BeautifulSoup(htmlfile, "lxml")

                            nodata = 'No daily or hourly history data available' in soup.text

                            if nodata == False:
                                obsTable = soup.find(id='obsTable')
                                result = obsTable.find_all("tr", attrs={"class": "no-metars"})
                                headings = obsTable.thead.find_all('th')
                                localTimezone = obsTable.thead.tr.th.span.next_element.strip('()')

                                for i in range(0, len(headings)-1):
                                    if 'Temp' in headings[i].text:
                                        temp_idx = i
                                    if 'Humidity' in headings[i].text:
                                        humid_idx = i
                                    if 'Pressure' in headings[i].text:
                                        pressure_idx = i

                        lastgameName = gameName

    ##                    minTimeDifference = timedelta(hours=24)

                    humidity = 0.0
                    temp = 0.0
                    pressure = 0.0
                    tdifftemp = '0.00'
                    tdiffrh = '0.00'
                    tdiffpres = '0.00'
                    
                    
                    # compares with desired date/time and extract weather data

                    if nodata == False:
                        (temp, tdifftemp) = getClosestMeas(temp_idx, 1, result, dtsv_id, year, month, day, localTimezone)
                        (humidity, tdiffrh) = getClosestMeas(humid_idx, 0, result, dtsv_id, year, month, day, localTimezone)
                        (pressure, tdiffpres) = getClosestMeas(pressure_idx, 1, result, dtsv_id, year, month, day, localTimezone)
                        
                    row['station{}code'.format(stationNum)] = code
                    row['station{}dist'.format(stationNum)] = bpdata[venue]['closest_ap{}_dist_km'.format(stationNum)]
                    
                    if nodata:
                        #row['t{}diff'.format(stationNum)] = '1440.00'
                        row['temp{}'.format(stationNum)] = '-1'
                        row['rh{}'.format(stationNum)] = '-1'
                        row['pres{}'.format(stationNum)] = '-1'
                        row['airdensity{}'.format(stationNum)] = '-1'
                    else:
                        row['t{}diffpres'.format(stationNum)] = tdiffpres
                        row['pres{}'.format(stationNum)] = pressure

                        if forecast == 'dome' or forecast == 'roof closed':
                            row['temp{}'.format(stationNum)] = csvtemp
                            row['t{}difftemp'.format(stationNum)] = '0.0'
                            row['rh{}'.format(stationNum)] = '50.0'
                            row['airdensity{}'.format(stationNum)] = getAirDensity(csvtemp, 50.0, pressure, altitude)
                        else:
                            row['temp{}'.format(stationNum)] = temp
                            row['t{}difftemp'.format(stationNum)] = tdifftemp
                            row['rh{}'.format(stationNum)] = humidity
                            row['t{}diffrh'.format(stationNum)] = tdiffrh
                            row['airdensity{}'.format(stationNum)] = getAirDensity(temp, humidity, pressure, altitude)
                        
                    writer.writerow(row)

    print('Parsing Completed.')
    elapsed = time.time() - start
    print('{:0.2f}'.format(elapsed))




