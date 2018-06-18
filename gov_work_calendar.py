import requests
from lxml import html
import csv
import datetime
from work_calendar import WorkCalendar
from dateutil.relativedelta import relativedelta


class GovCalendar(WorkCalendar):

    _startURL = 'http://data.gov.ru/opendata/7708660670-proizvcalendar'
    _XPathTemplate1 = '//a[contains(text(), "Последний набор")]'

    def __init__(self):
        super(GovCalendar, self).__init__()
        self.update()

    def _loadTextFromURL(self, URL):
        res = requests.get(URL)
        res.raise_for_status()
        res.encoding = 'UTF-8'
        return(res.text)

    def _getLastRef(self):
        text = self._loadTextFromURL(self._startURL)
        tree = html.fromstring(text)
        last = tree.xpath(self._XPathTemplate1)
        return([item.get('href') for item in last if 'UTF' in item.text_content()][0])
    
    def _parseData(self, headers, newData):
        for row in newData:
            year = int(row[0])
            for month in range(1, 13):
                days = row[month].split(',')
                holidays = [day.replace('+', '') for day in days if '*' not in day]
                startDate = datetime.date(year, month, 1)
                endDate = startDate + relativedelta(months=1)
                daysInMonth = (endDate-startDate).days
                monthData = {startDate + datetime.timedelta(days=d): {'holiday': str(d+1) in holidays} for d in range(0, daysInMonth)}
                super(GovCalendar, self).update(monthData)

    def update(self):
        csv_url = self._getLastRef()
        print('LOAD data from %s' % (csv_url,))

        with requests.Session() as s:
            download = s.get(csv_url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            headers = my_list[0]
            data = my_list[1:]
            try:
                self._parseData(headers, data)
            except Exception as e:
                print('PARSE ERROR', e)
                return({'status':'error'})

        return({'status':'updated'})