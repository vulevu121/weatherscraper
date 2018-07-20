import csv
import time
import math
import json
from parse_h import getTimezone
from datetime import datetime, timedelta, tzinfo
import pytz

pitchesfilename = 'WeatherCompTableRev_vu_part4.csv'

with open('ballparks.json', 'r') as f:
    bpdata = json.load(f)

print('Parsing file...')
with open(pitchesfilename, mode='r', newline='') as ifile:
    reader = csv.DictReader(ifile)
    fieldnames = reader.fieldnames
    fieldnames.append('localtime')

    with open('{}_parsed.csv'.format(pitchesfilename[0:-4]), mode='w', newline='') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            venue = row['venue']
            sv_id = row['sv_id']

            if sv_id[-2:] == '60':
                sv_id = '{}59'.format(sv_id[0:-2])
            row['sv_id'] = sv_id

            dtsv_id = datetime.strptime('{} UTC+0000'.format(sv_id), '%y%m%d_%H%M%S %Z%z')
            localtime = dtsv_id.astimezone(pytz.timezone(getTimezone(venue)))
            
            row['localtime'] = localtime
            writer.writerow(row)

            

            
