import numpy as np

confirmed = open("csse_covid_19_time_series\\time_series_19-covid-Confirmed.csv", "r")
deaths = open("csse_covid_19_time_series\\time_series_19-covid-Deaths.csv", "r")
recovered = open("csse_covid_19_time_series\\time_series_19-covid-Recovered.csv", "r")
files = [confirmed.readlines(), deaths.readlines(), recovered.readlines()]


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

print(data[0][212])
lenTable = []
index = 0
for lRow in data[1]:
    province = lRow[0] if lRow[0] == "" else f"{lRow[0]}, "
    print(f"{index}. {province}{lRow[1]}: {len(lRow)}: {lRow[2:]}")
    lenTable.append(len(lRow))
    index += 1


class Area:
    name = []
    date = []
    confirmed = []
    deaths = []
    recovered = []
    active = []
    latitude = ""
    longitude = ""

    def __init__(self, inputData, index):
        head = inputData[0][0]
        _name = inputData[0][index][:2]
        self.name = f"{_name[0]}, {_name[1]}" if _name[0] != "" else _name[1]
        self.date = head[4:]
        self.latitude = head[2]
        self.longitude = head[3]
        self.confirmed = self.toIntData(inputData[0][index][4:])
        self.deaths = self.toIntData(inputData[1][index][4:])
        self.recovered = self.toIntData(inputData[2][index][4:])
        self.active = self.calcActive()

    def toIntData(self, _data):
        result = []
        for i in range(len(_data)):
            try:
                result.append(int(_data[i]))
            except:

                result.append(int(_data[i].rstrip()))
        return result

    def calcActive(self):
        active = []
        for i in range(len(self.confirmed)):
            _confirmed = self.confirmed[i]
            _deaths = self.deaths[i]
            _recovered = self.recovered[i]
            active.append( _confirmed - _deaths - _recovered)
        return active

Poland = Area(data, 75)
#print(Poland.name)

class Covid:
    areas = []
    filtered  = []
    count = 0
    def __init__(self, inputData):
        self.count = len(inputData[0])-1
        for i in range(self.count):
            area = Area(inputData, i+1)
            self.areas.append(area)

    def list(self):
        self._list(self.areas)

    def _list(self, elements):
        for element in elements:
            print(f"{element.name}:: "
                  f"confirmed: {element.confirmed[-1]}, "
                  f"deaths: {element.deaths[-1]}, "
                  f"recovered: {element.recovered[-1]}, "
                  f"active: {element.active[-1]}")


    def printList(self):
        for i in range(self.count):
            print("")

    def getArea(self, name):
        print(f"\n{name}")
        result = list(filter(lambda x: name in x.name, self.areas))
        self._list(result)



w = Covid(data)
print(w.list())
print(w.getArea("United Kingdom"))
#w.getArea()
