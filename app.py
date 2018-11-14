#!/usr/bin/env python

import sys
from datetime import datetime, timedelta


# Opens file and organizes data in Dictionary
def openfile(filename):
    pilotsData = {}
    file = open(filename)
    lines = file.readlines()[1:]  # Skips first line
    for line in lines:
        line = line.split() # Turns line into list of 'words' 
        line.pop(2) # Removes '-' character from list
        if line[1] not in pilotsData:
            pilotsData.update({line[1]: [line[2], []]})
        pilotsData[line[1]][1].append([line[0],line[4],line[5]]) # Appends info for every lap to a list
    file.close()
    return pilotsData

# Convert string data to corresponding type
def convertData(pilotData):
    dataList = pilotData[1] # List of Lap Info
    for item in dataList:
        item[0] = datetime.strptime(item[0], '%H:%M:%S.%f')
        t = datetime.strptime(item[1], '%M:%S.%f')
        item[1] = timedelta(minutes=t.minute, seconds=t.second)
        item[2] = float(item[2].replace(",","."))

# Calculates Total of Laps, Total Time and Average Velocity
def calculatePilotReport(pilotValues):
    laps = len(pilotValues[1]) 
    totalTime = timedelta(seconds=0) 
    avgVelocity = 0
    bestLap = pilotValues[1][0][1]

    for item in pilotValues[1]:
        totalTime += item[1]
        avgVelocity += item[2]
        if item[1] < bestLap:
            bestLap = item[1]
    return [laps, totalTime, avgVelocity, bestLap]


def printReport(pilotsReport):
    print("Posição Chegada, Código Piloto, Nome Piloto, Qtde Voltas Completadas, Tempo Total de Prova, Velocidade Média, Melhor Volta")
    i = 1
    for pilot in pilotsReport:
        print("{0}, {1}, {2}, {3}, {4}, {5}, {6}".format(i, pilot[0], pilot[1], pilot[2], pilot[3], pilot[4], pilot[5], pilot[5]))
        i += 1
    
    # Best lap of all
    bestLapOfAll = sorted(pilotsReport, key=lambda x: (x[5]))[0]
    print("A melhor volta de toda a corrida foi a do {0} com tempo {1}".format(bestLapOfAll[1], bestLapOfAll[5]))
    

if __name__ == '__main__':
    pilotsReport = []

    try:
        result = openfile(sys.argv[1])
    except:
        print("Arquivo inválido ou inexistente")
        sys.exit(1)
    
    for k,v in result.items():
        convertData(v)
        pilotReport = [k, v[0]]
        pilotReport.extend(calculatePilotReport(v))
        pilotsReport.append(pilotReport)
    
    pilotsReport = sorted(pilotsReport, key=lambda x: (x[2], -x[3]), reverse=True)
    printReport(pilotsReport)
