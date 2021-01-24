import COVID19Py
from config import conf
from datetime import datetime


class CovidTracker:

    def getWorldData(self):
        covid19 = COVID19Py.COVID19(url="https://cvtapi.nl")
        return covid19.getLatest()

    def getCountryData(self, country):
        covid19 = COVID19Py.COVID19(url="https://cvtapi.nl")
        return covid19.getLocationByCountryCode(country)[0]

    def getData(self, country = 'world', format = 'json'):
        result = None

        if country == 'world':
            data = self.getWorldData()
        elif country:
            data = self.getCountryData(country)

        if format == 'json':
            result = data
        elif format == 'text':
            result = self.toText(data, country)

        return result

    def processCountryName(self, name):
        name = self.toLowwer(name)
        country = None
        
        for row in conf['countries']:
            if name == self.toLowwer(row['name']) or name in row['aliases']:
                country = row
                break

        return country

    def toLowwer(self, text):
        return text.strip().lower()

    def toText(self, data, country):
        if country == 'world':
            result  = ('Подтверждено случаев: ' + str(self.fmtNum(data['confirmed'])) + '\n' 
                    + 'Выздоровело: ' + str(self.fmtNum(data['recovered'])) + ' (не точно)\n' 
                    + 'Смертей: ' + str(self.fmtNum(data['deaths'])) + '\n'
            )
        else:
            result  = ('Всего случаев: ' + str(self.fmtNum(data['latest']['confirmed'])) + '\n' 
                    + 'Выздоровело: ' + str(self.fmtNum(data['latest']['recovered'])) + ' (не точно)\n' 
                    + 'Смертей: ' + str(self.fmtNum(data['latest']['deaths'])) + '\n'
                    + 'Население: ' + str(self.fmtNum(data['country_population'])) + '\n'
                    + 'Обновлено: ' + data['last_updated'][:10] + '\n'
            )

        return result

    @staticmethod
    def fmtNum(num):
        return "{:,d}".format(num).replace(',', ' ')
