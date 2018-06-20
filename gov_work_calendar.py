import requests
from lxml import html
import csv
import datetime
from work_calendar import WorkCalendar
from dateutil.relativedelta import relativedelta


class GovCalendar(WorkCalendar):

    _startURL = 'http://data.gov.ru/opendata/7708660670-proizvcalendar'
    _XPathTemplate1 = '//a[contains(text(), "Последний набор")]'
    _last_update = None

    def __init__(self):
        super(GovCalendar, self).__init__()
        self.update()

    def _loadTextFromURL(self, URL):
        res = requests.get(URL, timeout=10)
        res.raise_for_status()
        res.encoding = 'UTF-8'
        return(res.text)

    def _getLastRef(self):
        try:
            text = self._loadTextFromURL(self._startURL)
            tree = html.fromstring(text)
            last = tree.xpath(self._XPathTemplate1)
            return([item.get('href') for item in last if 'UTF' in item.text_content()][0])
        except Exception as e:
            return(None)

    def _parseData(self, headers, newData):
        for row in newData:
            year = int(row[0])
            for month in range(1, 13):
                days = row[month].split(',')
                holidays = [day.replace('+', '')
                            for day in days if '*' not in day]
                startDate = datetime.date(year, month, 1)
                endDate = startDate + relativedelta(months=1)
                daysInMonth = (endDate-startDate).days
                monthData = {startDate + datetime.timedelta(
                    days=d): {'holiday': str(d+1) in holidays} for d in range(0, daysInMonth)}
                super(GovCalendar, self).update(monthData)

    def update(self):
        csv_url = self._getLastRef()
        if not csv_url:
            return({'status': 'error', 'note': f'Failed URL: {self._startURL}'})
        print('LOAD data from %s' % (csv_url,))

        try:
            with requests.Session() as s:
                download = s.get(csv_url, timeout=10)
                decoded_content = download.content.decode('utf-8')
                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                my_list = list(cr)
                headers = my_list[0]
                data = my_list[1:]
                try:
                    self._parseData(headers, data)
                    print('Data loaded')
                except Exception as e:
                    print('PARSE ERROR', e)
                    return({'status': 'error'})
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
            return({'status': 'error', 'note': '{}: {}'.format(type(e).__name__, e)})

        return({'status': 'updated'})
