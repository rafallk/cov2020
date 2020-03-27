try:
    import LoadData as covid
except:
    import Documents.GitHub.Cov2020.Covid19.LoadData as covid

DATA = covid.GetData()
w = covid.Covid(DATA.data)
w.createEurope()
w.plotAreas("Europe")
