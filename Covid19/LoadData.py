import numpy as np
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
workDir = dir_path.split("Cov2020")[0]
dataDir = "Covid19\\csse_covid_19_data\\csse_covid_19_time_series\\"
workDir = f"{workDir}{dataDir}"

print(workDir)

confirmed = open(f"{workDir}time_series_19-covid-Confirmed.csv", "r")
deaths = open(f"{workDir}time_series_19-covid-Deaths.csv", "r")
recovered = open(f"{workDir}time_series_19-covid-Recovered.csv", "r")
files = [confirmed.read().split("\n"), deaths.read().split("\n"), recovered.read().split("\n")]

europeList = open("Definitions\\europe.txt").read().split("\n")

def delQuoteSign(_list):
    return np.append([_list[0].replace("\"", "") + _list[1].replace("\"", "")], _list[2:])


data = []
for lines in files:
    file = []
    for sRow in lines:
        aRow = []
        for element in sRow.split(","):
            aRow.append(element)
        aRow = delQuoteSign(aRow) if "\"" in aRow[0] else aRow
        file.append(aRow)
    data.append(file)

#print(data[0][212])
lenTable = []
index = 0
for lRow in data[1]:
    province = lRow[0] if lRow[0] == "" else f"{lRow[0]}, "
    #print(f"{index}. {province}{lRow[1]}: {len(lRow)}: {lRow[2:]}")
    lenTable.append(len(lRow))
    index += 1


class Area:

    def __init__(self, _name, head, _confirmed, _deaths, _recovered):
        self.name = f"{_name[0]}, {_name[1]}" if _name[0] != "" else _name[1]
        self.name = _name if isinstance(_name, str) else self.name
        self.date = head[4:]
        self.latitude = head[2]
        self.longitude = head[3]
        self.confirmed = _confirmed
        self.deaths = _deaths
        self.recovered = _recovered
        self.active = self.calcActive()
        self.attributes = []


    def calcActive(self):
        active = {}
        for i in range(len(self.confirmed)):
            _confirmed = self.confirmed[self.date[1]]
            _deaths = self.deaths[self.date[1]]
            _recovered = self.recovered[self.date[1]]
            active[self.date[i]] = (_confirmed - _deaths - _recovered)
        return active

    def MarkAsEurope(self, _area, _list, _marker):
        if _area in _list or f"{_area}, {_area}" in _list:
            self.attributes.append(_marker)

class Covid:
    europe = "Europe"

    def __init__(self, inputData):
        self.areas = []
        self.filtered = []
        self.count = len(inputData[0])-1
        _head = inputData[0][0]
        print(f"HEAD:: {_head}")
        self.head = _head
        for i in range(self.count):
            index = i+1

            _name = inputData[0][index][:2]
            _confirmed = self.toIntData(_head[4:], inputData[0][index][4:])
            _deaths = self.toIntData(_head[4:], inputData[1][index][4:])
            _recovered = self.toIntData(_head[4:], inputData[2][index][4:])
            area = Area(_name, _head, _confirmed, _deaths, _recovered)

            area.MarkAsEurope(area.name, europeList, self.europe)
            self.areas.append(area)

    def toIntData(self, date, _data):
        result = {}
        print(f"date len: {len(date)}")
        print(f"data len: {len(_data)}")
        y = len(_data) - len(date)
        for i in range(len(_data)-y):
            try:
                result[date[i]] = (int(_data[i]))
            except:
                result[date[i]] = (int(_data[i+y].rstrip()))
                pass
        return result

    def printList(self):
        self._list(self.areas)

    def _list(self, elements):
        for element in elements:
            key = element.date[-1]
            print(f"{element.name}:: "
                  f"confirmed: {element.confirmed[key]}, "
                  f"deaths: {element.deaths[key]}, "
                  f"recovered: {element.recovered[key]}, "
                  f"active: {element.active[key]}" + ", " + self.europe if self.europe in element.attributes else ""
                  )

    def getArea(self, name):
        result = list(filter(lambda x: name in x.name, self.areas))
        self._list(result)
        return result

    def joinAreaNames(self, _list):
        ret = ""
        for i in _list:
            print(i.name + " " + str.join(", ", i.attributes))

    def printEurope(self):
        for country in self.areas:
            if self.europe in country.attributes:
                print(country.name)

    def createEurope(self):
        _date = self.areas[0].date
        _len = len(_date)
        confirmed_buf = {k: 0 for k in _date}
        deaths_buf = {k: 0 for k in _date}
        recovered_buf = {k: 0 for k in _date}
        for i in range(self.count):
            if self.europe in self.areas[i].attributes:
                confirmed_buf = {key: (confirmed_buf[key] + self.areas[i].confirmed[key]) for key in _date}
                deaths_buf = {key: (deaths_buf[key] + self.areas[i].deaths[key]) for key in _date}
                recovered_buf = {key: (recovered_buf[key] + self.areas[i].recovered[key]) for key in _date}
        area = Area(self.europe, self.head, confirmed_buf, deaths_buf, recovered_buf)
        area.attributes.append("Continent")
        self._list([area])
        self.areas.append(area)


    def getEurope(self):
        result = list(filter(lambda x: x.europe in x.attributes, self.areas))
        self._list(result)

a = ["a", "b", "c"]
b = ["1", "2", "3"]
d = ["5", "6", "7"]
c = {k: v1+v2 for (k, v1, v2) in zip(a, b, d)}
e = {k: v for (k, v) in zip(a, [0]*len(a))}
e = {k: 0 for k in a}
print(f"test:: {c}")
print(f"test:: {e}")

w = Covid(data)
# w.printList()

#print(w.list())
country = w.getArea("Germany")[0]
print(country.name + ": " + str(country.confirmed))
w.createEurope()
aa = w.getArea("Europe")[0]
print(aa.name + ": " + str(aa.confirmed))


# area = "United Kingdom"
# print(area in europeList)
# print(area in europeList or f"{area}, {area}" in europeList)

# w.printEurope()
