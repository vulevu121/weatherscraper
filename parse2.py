from bs4 import BeautifulSoup
from collections import OrderedDict

htmlPath = 'C:\\Users\\Vu\\Documents\\weatherscraper\\wunderground\\2018_3_29_KHWD.html'

html = open(htmlPath, encoding='utf-8')

soup = BeautifulSoup(html, 'lxml')
table = soup.find(name='table', class_='tablesaw-sortable', id='history-observation-table')

spans = table.find_all(name='span')

i = 11
data = []
while i < len(spans):
    row = spans[i:i+27]
    data.append([x.text.replace('\n', '').strip() for x in row])
    i += 27

weatherDict = OrderedDict()
for row in data:
    weatherDict[row[0]] = {
        'Temperature': row[1],
        'Dew Point': row[4],
        'Humidity': row[7],
        'Wind': row[10],
        'Wind Speed': row[11],
        'Wind Gust': row[14],
        'Pressure': row[17],
        'Precip': row[20],
        'Precip Accum': row[23],
        'Condition': row[26]
    }
