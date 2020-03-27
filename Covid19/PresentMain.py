try:
    import LoadData as covid
except:
    import Documents.GitHub.Cov2020.Covid19.LoadData as covid

DATA = covid.GetData()
w = covid.Covid(DATA.data)
w.createEurope()
w.createRegion("China")
w.createRegion("US")
w.createRegion("Canada")

w.plotAreas(["Europe", "US", "China", "Italy"])
w.plotAreasPercent(["Europe", "US", "China", "Italy"])
#
w.plotAreas(["Poland", "Switzerland", "Germany", "India", "Russia", "Brazil", "Singapore", "Taiwan", "Hubei, China"])
w.plotAreasPercent(["Poland", "Switzerland", "Germany", "India", "Russia", "Brazil", "Singapore", "Taiwan", "Hubei, China"])
w.plotAreas(["Czech", "France", "Spain", "Canada", "Japan", "Korea", "Hong Kong", "Madagascar", "Argentina"])

# Poland = w.getArea("Poland")
# print(Poland.name + ": " + str(Poland.active))
# China = w.getArea("China")
# print(China.name + ": " + str(China.confirmed))
