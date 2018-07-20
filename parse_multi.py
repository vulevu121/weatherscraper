# Written by Vu Le
# Spring 2018
# Prof. Glenn Healey

from parse import parse
from multiprocessing import Pool
import time
from nosleep import *
import os

if __name__ == '__main__':
    with Pool(4) as p:
        args1 = [['WeatherCompTableRev_vu_part1.csv', '1'],
                      ['WeatherCompTableRev_vu_part2.csv', '1'],
                      ['WeatherCompTableRev_vu_part3.csv', '1'],
                      ['WeatherCompTableRev_vu_part4.csv', '1']]
        args2 = [['WeatherCompTableRev_vu_part1_parsed.csv', '2'],
                      ['WeatherCompTableRev_vu_part2_parsed.csv', '2'],
                      ['WeatherCompTableRev_vu_part3_parsed.csv', '2'],
                      ['WeatherCompTableRev_vu_part4_parsed.csv', '2']]
        args3 = [['WeatherCompTableRev_vu_part1_parsed_parsed.csv', '3'],
                      ['WeatherCompTableRev_vu_part2_parsed_parsed.csv', '3'],
                      ['WeatherCompTableRev_vu_part3_parsed_parsed.csv', '3'],
                      ['WeatherCompTableRev_vu_part4_parsed_parsed.csv', '3']]
        
        # in Windows, prevent the OS from sleeping while we run
        osSleep = None
        if os.name == 'nt':
            osSleep = WindowsInhibitor()
            osSleep.inhibit()

        start = time.time()
        print('Parsing file...')
        p.map(parse, args1)
        p.map(parse, args2)
        p.map(parse, args3)

        print('Parsing Completed.')
        elapsed = time.time() - start
        print('{:0.2f}'.format(elapsed))

        # return to normal power management
        if osSleep:
            osSleep.uninhibit()
