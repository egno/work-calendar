from datetime import date


class WorkCalendar(object):
    
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, data = None):
        self.data = {}
        self._defaultDay = {
            'holiday': None,
            'default': True
            }

        if data:
            self.update(data)

    def _generateDate(self, requestDate):
        return {
            'holiday': requestDate.weekday() > 5,
            'default': True
            }
        
    def date(self, requestDate, strong=False):
        default = self._defaultDay
        if not strong:
            default = self._generateDate(requestDate)
        result = self.data.get(requestDate, default)
        return(result)


    def update(self, data):
        self.data.update(data)



