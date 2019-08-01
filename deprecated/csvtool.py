# Written by Vu Le
# Spring 2018
# Prof. Glenn Healey

import csv

def csvsplit(infile, rowsize=176100, headersall=True):
    file_count = 1
    row_total = 704367
    
    with open(infile, mode='r', newline='') as ifile:
        reader = csv.DictReader(ifile)
        header = reader.fieldnames

        while(reader.line_num < row_total):
                
            outfile = '{}_part{}.csv'.format(infile[0:-4], file_count)
            with open(outfile, mode='w', newline='') as ofile:
                writer = csv.DictWriter(ofile, fieldnames=header)
                if(file_count == 1 or headall):
                    writer.writeheader()

                for row in reader:
                    writer.writerow(row)
                    if(reader.line_num % rowsize == 0 and reader.line_num > 0):
                        file_count = file_count + 1
                        break
    
def csvjoin(filelist, outputfile):
    with open(outputfile, mode='w', newline='') as ofile:
        writer = 0

        for eachFile in filelist:
            start = 0
            with open(eachFile, mode='r', newline='') as ifile:
                reader = csv.DictReader(ifile)
                
                if(writer == 0):
                    header = reader.fieldnames
                    writer = csv.DictWriter(ofile, fieldnames=header)
                    writer.writeheader()
                    
                for row in reader:
                    writer.writerow(row)
                    
