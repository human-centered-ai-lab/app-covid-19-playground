from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
from scipy import signal
import psycopg2 as ps
import seaborn as sns
import pandas as pd
import numpy  as np
import requests
import math
import json

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


r = requests.get(url = "https://pomber.github.io/covid19/timeseries.json") 
data = r.json() 

countries = sorted(data.keys())
print ("ALL COUNTRIES WITH DATA AVAILABLE at pomber.github.io")
#print (countries)

countriesOfInterest = ['Austria', 'Belgium','Czechia', 'Denmark', 'Finland', 'France', 'Germany', 'Hungary',  'Italy', 'Malta','Netherlands',  'Portugal', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'US', 'United Kingdom']
population = {}
for c in countriesOfInterest:
  r = requests.get(url = "https://restcountries.eu/rest/v2/name/" + c) 
  cinforeq = r.json() 
  if ( r.status_code == 200):
      population[c] = cinforeq[0]['population']
  else:
      population[c] = 999999999999999999999999
population.update ({'Czechia' : 10703551})
population.update ({'US' : 330467650})

print ("COUNTRIES OF INTEREST WITH POPULATION")
print (population)


startDate = date(2020, 3, 7)
endDataForAnimation = ( datetime.now()+timedelta(days=1)).date()
endDateForDiagrams = []     

for sd in daterange(date(2020, 3, 14), endDataForAnimation):
    endDateForDiagrams.append(sd)

lastImageIndex = len(endDateForDiagrams) - 1
stayStaticInTheEnd = 32

width_in_inches  = 24
height_in_inches = 16
dots_per_inch = 70



for timewindowindex, endDateInDiagram in enumerate(endDateForDiagrams):
 
    plt.figure( figsize=(width_in_inches, height_in_inches), dpi=dots_per_inch)

    datesToInspect = []
    x_axis_data = [];
    for single_date in daterange(startDate, endDateInDiagram):
        x_axis_data.append(single_date.strftime("%d.%m"))
        datesToInspect.append(single_date.strftime("%Y-%-m-%-d"))

    lines = []
    labels = []
    numberToOrder = {}
    i = 0
    plt.ylim(1, 10000)
    for c in countriesOfInterest:
        y_axis_data = []
        for dataindex in datesToInspect:
            datafromonecontry = data[c]
            for daydata in datafromonecontry:
                #print (daydata['date'], dataindex)
                if daydata['date'] == dataindex:
                    cc = daydata['confirmed']
                    normalizedcc = cc * 1000000 / population[c]
                    v = normalizedcc
                    numberToOrder[i] = v
                    y_axis_data.append(v)
        ls = 'solid' if c == 'Austria' else '--'    
        lines, = plt.plot(x_axis_data,  y_axis_data, label=c, linestyle=ls, marker='o')
        labels.append (c)
        plt.legend( )
        i = i + 1

    LabelOrdering = []
    for e in sorted(numberToOrder.items(), key=lambda x: x[1], reverse=True):
        LabelOrdering.append (e[0])

    plt.yscale('log')
    plt.xlabel("date")
    plt.ylabel("number of cases per one million inhabitants")
    plt.grid(True)

    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend([handles[idx] for idx in LabelOrdering],[labels[idx] for idx in LabelOrdering], loc='upper left')
    #plt.show()
    plt.savefig('casesabsolut/cases-absolut' + str(timewindowindex).zfill(2) + '.png')
    if (timewindowindex== lastImageIndex):
        for i in range (stayStaticInTheEnd):
            plt.savefig('casesabsolut/cases-absolut' + str(timewindowindex+i).zfill(2) + '.png')
    plt.close()



#
# GROWTH
#

startDate = date(2020, 3, 14)
endDateForDiagrams = []
for sd in daterange(date(2020, 3, 20), endDataForAnimation):
    endDateForDiagrams.append(sd)

dateIndexMapper = []
datesToConsider = []

for sd in daterange(date(2020, 3, 5), endDataForAnimation):
    datesToConsider.append (sd)

for sd in reversed (datesToConsider ):
    dateIndexMapper.append (sd.strftime("%Y-%-m-%-d"))

#print (dateIndexMapper)


lastImageIndex = len(endDateForDiagrams) - 1
stayStaticInTheEnd = 32

deltaInDays = 3
timerange = len(endDateForDiagrams)

for timewindowindex, endDateForDiagram  in  enumerate(endDateForDiagrams):

    plt.figure( figsize=(width_in_inches, height_in_inches), dpi=dots_per_inch)

    datesToInspect = []
    x_axis_data = [];
    for single_date in daterange(startDate, endDateForDiagram ):
        x_axis_data.append(single_date.strftime("%d.%m"))
        datesToInspect.append(single_date)

    lines = []
    labels = []

    plt.figure( figsize=(width_in_inches, height_in_inches), dpi=dots_per_inch)
    numberOfDays = len(datesToInspect)
    numberToOrder = {}
    i = 0
    plt.ylim(1, 75)

    dateIndexReverse = len(endDateForDiagrams) - timewindowindex
#    print ('======== DIAGRAM NR  ', timewindowindex)

    for c in countriesOfInterest:
        y_axis_data = []
        for dataindex, datestringend in enumerate(datesToInspect):

            dateIndexReverse = len(endDateForDiagrams) + len(datesToInspect) - dataindex - timewindowindex  
            datafromonecontry = data[c]

            fromcc = 0
            tocc  = 0
            
            for daydata in datafromonecontry:
                if daydata['date'] == dateIndexMapper [dateIndexReverse+deltaInDays]:
                    fromcc = daydata['confirmed']
            for daydata in datafromonecontry:
                if daydata['date'] == dateIndexMapper [dateIndexReverse]:
                    tocc  = daydata['confirmed']

            if fromcc  == 0:
                v = 0
            else:       
                v = 100 * (tocc-fromcc) / fromcc  / deltaInDays
                    
            numberToOrder[i] = v
            y_axis_data.append(v)

#            print ( '         from = ', dateIndexMapper [dateIndexReverse-deltaInDays], "to = ",dateIndexMapper [dateIndexReverse], "GR = ", v)

        ls = 'solid' if c == 'Austria' else 'dotted'
        lines, = plt.plot(x_axis_data,  y_axis_data, label=c, linestyle=ls)
        labels.append (c)
        plt.legend()
        i = i + 1 

    LabelOrdering = []
    for e in sorted(numberToOrder.items(), key=lambda x: x[1], reverse=True):
        LabelOrdering.append (e[0])

    plt.xlabel("date")
    plt.ylabel("estimate of growth rate (in perzent per day), time window 3 days")
    plt.grid(True)
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend([handles[idx] for idx in LabelOrdering],[labels[idx] for idx in LabelOrdering], loc='upper left')
    plt.savefig('casesgrowth/cases-growth' + str(timewindowindex).zfill(2) + '.png')
    if (timewindowindex == lastImageIndex):
        for i in range (stayStaticInTheEnd):
            plt.savefig('casesgrowth/cases-growth' + str(timewindowindex+i).zfill(2) + '.png')
    plt.close()

   
    
   