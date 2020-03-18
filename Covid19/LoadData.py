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
files = [confirmed.readlines(), deaths.readlines(), recovered.readlines()]

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
        self.date = head[4:]
        self.latitude = head[2]
        self.longitude = head[3]
        self.confirmed = _confirmed
        self.deaths = _deaths
        self.recovered = _recovered
        self.active = self.calcActive()
        self.attributes = []



    def calcActive(self):
        active = []
        for i in range(len(self.confirmed)):
            _confirmed = self.confirmed[i]
            _deaths = self.deaths[i]
            _recovered = self.recovered[i]
            active.append(_confirmed - _deaths - _recovered)
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
        for i in range(self.count):
            index = i+1
            _head = inputData[0][1]
            self.head = _head
            _name = inputData[0][index][:2]
            _confirmed = self.toIntData(inputData[0][index][4:])
            _deaths = self.toIntData(inputData[1][index][4:])
            _recovered = self.toIntData(inputData[2][index][4:])
            area = Area(_name, _head, _confirmed, _deaths, _recovered)

            area.MarkAsEurope(area.name, europeList, self.europe)
            self.areas.append(area)

    def toIntData(self, _data):
        result = []
        for i in range(len(_data)):
            try:
                result.append(int(_data[i]))
            except:
                result.append(int(_data[i].rstrip()))
        return result

    def printList(self):
        self._list(self.areas)

    def _list(self, elements):
        for element in elements:
            print(f"{element.name}:: "
                  f"confirmed: {element.confirmed[-1]}, "
                  f"deaths: {element.deaths[-1]}, "
                  f"recovered: {element.recovered[-1]}, "
                  f"active: {element.active[-1]}" + ", " + self.europe if self.europe in element.attributes else ""
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
        _len = len(self.areas[0].confirmed)
        _confirmed = [0] * _len
        _deaths = [0] * _len
        _recovered = [0] * _len
        for i in range(self.count):
            if self.europe in self.areas[i].attributes:
                _confirmed = [x + y for x, y in zip(_confirmed, self.areas[i].confirmed)]
                _deaths = [x + y for x, y in zip(_deaths, self.areas[i].deaths)]
                _recovered = [x + y for x, y in zip(_recovered, self.areas[i].recovered)]
        area = Area(self.europe, self.head, _confirmed, _deaths, _recovered)
        area.attributes.append("Continent")
        self._list([area])
        self.areas.append(area)


    def getEurope(self):
        result = list(filter(lambda x: x.europe in x.attributes, self.areas))
        self._list(result)



w = Covid(data)
# w.printList()

#print(w.list())
country = w.getArea("Italy")[0]
print(country.name + ": " + str(country.confirmed))
w.createEurope()
# area = "United Kingdom"
# print(area in europeList)
# print(area in europeList or f"{area}, {area}" in europeList)

# w.printEurope()
