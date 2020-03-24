import numpy as np
import os
import math
import datetime
import matplotlib.pyplot as plt


dir_path = os.path.dirname(os.path.realpath(__file__))
workDir = dir_path.split("Cov2020")[0]
dataDir = "Covid19\\csse_covid_19_data\\csse_covid_19_time_series\\"
workDir = f"{workDir}{dataDir}"

confirmed = open(f"{workDir}time_series_19-covid-Confirmed.csv", "r")
deaths = open(f"{workDir}time_series_19-covid-Deaths.csv", "r")
recovered = open(f"{workDir}time_series_19-covid-Recovered.csv", "r")
files = [confirmed.read().split("\n"), deaths.read().split("\n"), recovered.read().split("\n")]

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

lenTable = []
index = 0
for lRow in data[1]:
    province = lRow[0] if lRow[0] == "" else f"{lRow[0]}, "
    lenTable.append(len(lRow))
    index += 1

try:
    europeList = open("Definitions\\europe.txt").read().split("\n")
    population = open("Definitions\\populations.txt").read().split("\n")
except:workDir

newDir = "C:\\Users\\rafal\\Documents\\GitHub\Cov2020\\Covid19\\"
europeList = open(f"{newDir}Definitions\\europe.txt").read().split("\n")
population = open(f"{newDir}Definitions\\populations.txt").read().split("\n")

class GetData:
    def __init__(self, ):
        self.data = data
        self.europeList = europeList
        self.population = population

########################################################################################################################


class Population:
    def __init__(self, region):
        reg = region.split("\t")
        try:
            self.number = int(reg[0])
        except:
            self.number = 1000
        self.name = (reg[1].split("[")[0] if "[" in reg[1] else reg[1])[1:]
        try:
            self.population = int(reg[2].replace(",", ""))
        except:
            self.population = int(reg[2])

########################################################################################################################


class Area:

    def __init__(self, _name, head, _confirmed, _deaths, _recovered, regionCount):
        x = [y[regionCount-1 if regionCount > 1 else 0:regionCount+1 if len(y) - regionCount > 1 else regionCount] for y in data]
        self.id = regionCount
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
            _confirmed = self.confirmed[self.date[i]]
            _deaths = self.deaths[self.date[i]]
            _recovered = self.recovered[self.date[i]]
            active[self.date[i]] = (_confirmed - _deaths - _recovered)
        return active

    def MarkAsEurope(self, _area, _list, _marker):
        if _area in _list or f"{_area}, {_area}" in _list:
            self.attributes.append(_marker)

########################################################################################################################


class Covid:
    europe = "Europe"

    def __init__(self, inputData):
        self.regionCount = 0
        self.population = []
        self.areas = []
        self.filtered = []
        self.count = len(inputData[0])-2
        self.head = inputData[0][0]
        self.date = self.head[4:]
        self.calcPopulation()
        for i in range(1, self.count):
            _name = inputData[0][i][:2]
            _confirmed = self.toIntData(self.date, inputData[0][i][4:])
            _deaths = self.toIntData(self.date, inputData[1][i][4:])
            _recovered = self.toIntData(self.date, inputData[2][i][4:])
            area = Area(_name, self.head, _confirmed, _deaths, _recovered, self.regionCount)
            area.MarkAsEurope(area.name, europeList, self.europe)
            self.areas.append(area)
            self.regionCount += 1

    def calcPopulation(self):
        for region in population:
            self.population.append(Population(region))

    def toIntData(self, date, _data):
        result = {}
        y = len(_data) - len(date)
        for i in range(len(_data)-y):
            try:
                result[date[i]] = (int(_data[i]))
            except:
                try:
                    result[date[i]] = (int(_data[i+y].rstrip()))
                except:
                    result[date[i]] = 0

        return result

    def printList(self):
        self._list(self.areas)

    def _list(self, elements):
        printStr = ""
        for element in elements:
            key = element.date[-1]
            printBuf = (f"{element.name}:: "
                  f"confirmed: {element.confirmed[key]}, "
                  f"deaths: {element.deaths[key]}, "
                  f"recovered: {element.recovered[key]}, "
                  f"active: {element.active[key]}" + ", " + (self.europe if self.europe in element.attributes else ""))
            printStr = f"{printStr}{printBuf}\n"
        print(printStr)

    def getArea(self, name):
        result = list(filter(lambda x: name in x.name, self.areas))
        self._list(result)
        return result[0]

    def plotArea(self, name):
        area_buf = list(filter(lambda x: name in x.name, self.areas))[0]
        plt.plot(range(len(area_buf.date)), [area_buf.confirmed[key] for key in area_buf.date])
        plt.plot(range(len(area_buf.date)), [area_buf.recovered[key] for key in area_buf.date])
        plt.plot(range(len(area_buf.date)), [area_buf.deaths[key] for key in area_buf.date])
        plt.plot(range(len(area_buf.date)), [area_buf.active[key] for key in area_buf.date])
        plt.show()

    def plotAreas(self, names, allIncluded=False, maxSubplots=9, ppm=False, byAttribute=False):
        if allIncluded:
            name = names if isinstance(names, str) else names[0]
            names = [y.name for y in filter(lambda x: name in x.name, self.areas)]

        ms = maxSubplots
        count = len(names)
        _iter = math.floor(count/ms)
        _iter = (_iter * [ms]) + [count % ms]

        i = ms + 1
        j = 0
        plt.figure(figsize=(20, 10))
        for name in names:
            if i > ms:
                count = _iter[j]
                h = math.ceil(math.sqrt(count))
                v = math.ceil(count / h)
                i = 1
                j += 1
                if j > 1:
                    plt.legend()
                    plt.show()
            pop = 1
            ylabel = "People"
            if ppm:
                popName = name[:-1] if name[-1] == "," else name
                popName = "United States" if popName == "US" else popName
                pop = list(filter(lambda x: popName in x.name, self.population))[0].population / 1000000
                ylabel = "People per million"

            try:
                area_buf = list(filter(lambda x: name is x.name, self.areas))[0]
            except:
                area_buf = list(filter(lambda x: name in x.name, self.areas))[0]

            plt.subplot(int(f"{v}{h}{i}"))
            plt.plot(range(len(area_buf.date)), [area_buf.confirmed[key]/pop for key in area_buf.date], label="confirmed")
            plt.plot(range(len(area_buf.date)), [area_buf.recovered[key]/pop for key in area_buf.date], label="recovered")
            plt.plot(range(len(area_buf.date)), [area_buf.deaths[key]/pop for key in area_buf.date], label="deaths")
            plt.plot(range(len(area_buf.date)), [area_buf.active[key]/pop for key in area_buf.date], label="active")
            plt.ylabel(ylabel)
            plt.title(area_buf.name)
            i += 1
        plt.legend()
        plt.show()

    def plotAreasPercent(self, names, allIncluded=False, maxSubplots=9, ):
        self.plotAreas(names, allIncluded, maxSubplots, True)



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
        for i in range(len(self.areas)):
            if self.europe in self.areas[i].attributes:
                confirmed_buf = {key: (confirmed_buf[key] + self.areas[i].confirmed[key]) for key in _date}
                deaths_buf = {key: (deaths_buf[key] + self.areas[i].deaths[key]) for key in _date}
                recovered_buf = {key: (recovered_buf[key] + self.areas[i].recovered[key]) for key in _date}
        area = Area(self.europe, self.head, confirmed_buf, deaths_buf, recovered_buf, self.regionCount)
        area.calcActive()
        area.attributes.append("Continent")
        self._list([area])
        self.areas.append(area)

    def createRegion(self, name):
        area_buf = list(filter(lambda x: name in x.name, self.areas))
        confirmed_buf = {k: 0 for k in self.date}
        deaths_buf = {k: 0 for k in self.date}
        recovered_buf = {k: 0 for k in self.date}
        for i in range(len(area_buf)):
                confirmed_buf = {key: (confirmed_buf[key] + area_buf[i].confirmed[key]) for key in self.date}
                deaths_buf = {key: (deaths_buf[key] + area_buf[i].deaths[key]) for key in self.date}
                recovered_buf = {key: (recovered_buf[key] + area_buf[i].recovered[key]) for key in self.date}
        area = Area(name, self.head, confirmed_buf, deaths_buf, recovered_buf, self.regionCount)
        area.calcActive()
        area.attributes.append(name)
        self._list([area])
        self.areas.append(area)

    def getEurope(self):
        result = list(filter(lambda x: x.europe in x.attributes, self.areas))
        self._list(result)

########################################################################################################################

DATA = GetData()
w = Covid(DATA.data)
w.createEurope()
w.createRegion("China")
w.createRegion("US")
w.createRegion("Canada")
w.plotAreas(["Europe", "US", "China", "Italy"])
w.plotAreasPercent(["Poland", "Switzerland", "Germany", "US", "China", "Europe", "Singapore", "Taiwan", "Hubei, China"], maxSubplots=9)
w.plotAreas(["Poland", "Switzerland", "Germany", "US", "China", "Europe", "Singapore", "Taiwan", "Hubei, China"])
#w.plotAreas(["Czech", "France", "Spain", "Canada", "Japan", "Korea", "Hong Kong", "Madagascar", "United Kingdom,", "China"])

# Poland = w.getArea("Poland")
# print(Poland.name + ": " + str(Poland.active))
# China = w.getArea("China")
# print(China.name + ": " + str(China.confirmed))
