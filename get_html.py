# Written by Vu Le
# Spring 2018
# Prof. Glenn Healey

import requests
import csv
import time
import json
import os.path

start = time.time()

requestDelay = 1

# ===== REQUIRED ======
# list of pitches to extract to weather data
pitches_csv = 'WeatherCompTableRev_vu.csv'

# total number of rows in pitches_csv including fieldnames row
row_count = 704367
# ==================


# json that contains venue information
with open('ballparks.json', 'r') as f:
    bpdata = json.load(f)

print('Loading CSV file...')
with open(pitches_csv, newline='') as f1:
    reader = csv.DictReader(f1)
    print('Grabbing HTML files...')

    # initialization
    lastgameName = 'none'
    gameName = ''

    # for displaying progress percent
    percent = 5
    row_mod = row_count // 20

    # specify a row to start from if needed
    startRow = 0
    
    for row in reader:
        if reader.line_num % row_mod == 0:
            print('Progress: {} % / Line: {}'.format(percent, reader.line_num))
            percent = percent + 5

        ap_list = ['closest_ap1_code', 'closest_ap2_code', 'closest_ap3_code']

        if (reader.line_num >= startRow):
            gameName = row['gameName']
            venue = row['venue']
            gameNameSplit = gameName.split(sep='_')

            YEAR = gameNameSplit[1]
            MONTH = gameNameSplit[2]
            DAY = gameNameSplit[3]
            URL = 'https://www.wunderground.com/cgi-bin/findweather/getForecast'

            # if gameName is different than the last one, then pull html
            if gameName != lastgameName:
                for each in ap_list:
                    CODE = bpdata[venue][each]

                    params = {
                            'airportorwmo': 'query',
                            'historytype':  'DailyHistory',
                            'backurl':      '/history/index.html',
                            'code':         CODE,
                            'day':          DAY,
                            'month':        MONTH,
                            'year':         YEAR,
                            }

                    htmlfile = 'wunderground/{}_{}_{}_{}.html'.format(YEAR, MONTH, DAY, CODE)

                    # if file exists already then skip
                    if os.path.isfile(htmlfile):
                        continue

                    r = requests.get(URL, params=params)

                    with open(htmlfile, mode='w', encoding='utf-8') as f:
                        f.write(r.text)

                    lastgameName = gameName

                    # delay per request to prevent wunderground from timing out
                    time.sleep(requestDelay)

print('Progress: DONE...')
elapsed = time.time() - start
print('{:0.2f}'.format(elapsed))
