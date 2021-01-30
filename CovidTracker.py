import COVID19Py
from countries import countries


class CovidTracker:
    covid19 = COVID19Py.COVID19(url="https://cvtapi.nl")

    def getWorldData(self):
        return self.covid19.getLatest()

    def getCountryData(self, country):
        # return self.covid19.getLocationByCountryCode(country, timelines=True)[0]
        return self.covid19.getLocationByCountryCode(country)[0]

    def getData(self, country='world', format='json'):
        result = None
        data = None

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
        name = self.toLower(name)
        country = None

        for row in countries:
            if name == self.toLower(row['name']) or name == self.toLower(row['code']) or name in row['aliases']:
                country = row
                break

        return country

    def toLower(self, text):
        return text.strip().lower()

    def toText(self, data, country):
        if country == 'world':
            result = ('Подтверждено случаев: ' + str(self.fmtNum(data['confirmed'])) + '\n'
                      # + 'Выздоровело: ' + str(self.fmtNum(data['recovered'])) + ' (не точно)\n'
                      + 'Смертей: ' + str(self.fmtNum(data['deaths'])) + '\n'
                      )
        else:
            result = ('Всего случаев: ' + str(self.fmtNum(data['latest']['confirmed'])) + '\n'
                      # + 'Выздоровело: ' + str(self.fmtNum(data['latest']['recovered'])) + ' (не точно)\n'
                      + 'Смертей: ' + str(self.fmtNum(data['latest']['deaths'])) + '\n'
                      + 'Население: ' + str(self.fmtNum(data['country_population'])) + '\n'
                      + 'Обновлено: ' + data['last_updated'][:10] + '\n'
                      )

        return result

    @staticmethod
    def fmtNum(num):
        return "{:,d}".format(num).replace(',', ' ')
