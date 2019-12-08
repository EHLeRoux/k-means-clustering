
import pandas as pd 
import numpy as np 
import random as rd
import pprint as pp
import matplotlib.pyplot as plt 
import itertools
import math
import matplotlib

'''
Implementing the k-means clustering algorithm from scratch 
Author: Eduard Le Roux
'''

fileName1 = "data1953.csv"
fileName2 = "data2008.csv"
fileName3 = "dataBoth.csv"


# Reading in the .csv files and saving them as dataframes
def read():
    userFileSelection = int (input ("Which file do you want to read in? 1: 1953 dataset or 2: 2008 dataset or 3: dataset of both"))
    
    while (True):
        if userFileSelection == 2:
            dataFrame = pd.read_csv(fileName2)
            dataFrameCountries = list(dataFrame['Countries'])
            dataFrameBirthRates = list (dataFrame['BirthRate(Per1000 - 2008)'])
            dataFrameLifeExpectancy = list (dataFrame['LifeExpectancy(2008)'])
            return dataFrameCountries, dataFrameBirthRates, dataFrameLifeExpectancy
            break;
        elif userFileSelection == 1: 
            dataFrame = pd.read_csv(fileName1)
            dataFrameCountries = list(dataFrame['Countries'])
            dataFrameBirthRates = list (dataFrame['BirthRate(Per1000 - 1953)'])
            dataFrameLifeExpectancy = list (dataFrame['LifeExpectancy(1953)'])
            return dataFrameCountries, dataFrameBirthRates, dataFrameLifeExpectancy
            break;
        elif userFileSelection == 3: 
            dataFrame = pd.read_csv(fileName3)
            dataFrameCountries = list(dataFrame['Countries'])
            dataFrameBirthRates = list (dataFrame['BirthRate(Per1000)'])
            dataFrameLifeExpectancy = list (dataFrame['LifeExpectancy'])
            return dataFrameCountries, dataFrameBirthRates, dataFrameLifeExpectancy
            break;
            
        else: 
            userFileSelection = int (input ("Please select a valid input 1: 1953 dataset or 2: 2008 dataset or 3: data set of both"))


# Calculating the distance between two points
def euc_distance (xi, xj, yi, yj):
    distance = np.sqrt(np.square(xj - xi) + np.square(yj - yi))
    return distance


# Calculating the mean of two lists
def mean (xList, yList):
    xMean = np.mean(xList)
    yMean = np.mean(yList)
    return xMean, yMean

'''
Here we do the main k-means algorithm. 
Calling the top three functions where needed.
Thought Process of list: for each cluster - > [[[Country, xCoor, yCoor], [Country2, xCoor2, yCoor2]], [[Countr3, xCoor3, yCoor3]]]
'''


def k_means (CountriesList, BirthRateList, LifeExpectancyList):
    
    # Generating cluster list which will store all the x and y points
    userInput = int (input("How many clusters do you want?"))
    iterationInput = int (input ("How many iterations do you want? "))
    firstClusterList = [[] for i in range(userInput)] 
    randomPointGeneratorList = []
    
    # Generating randomPoints
    for i in range(userInput):
        randomPoint = rd.randint(0, len(BirthRateList) - 1)
        randomPointGeneratorList.append(randomPoint)
    
    # Checking for duplicates in the list
    for i in randomPointGeneratorList: 
        for j in 1, randomPointGeneratorList:   
            if i == j: 
                randomPoint = rd.randint(0, len(BirthRateList) - 1)
                randomPointGeneratorList.insert(j, randomPoint)
                
        if i == len(randomPointGeneratorList): 
            break;
        
    # Printing out the random countries with their birth rates and life expectancies
    for i in randomPointGeneratorList: 
        print("Country: {}".format (CountriesList[i]))
        print("BirthRate: {}".format(BirthRateList[i]))  
        print("LifeExpectancy: {} \n".format(LifeExpectancyList[i]))
    pp.pprint(firstClusterList)
    
    # Calculating the EUC distance of points to the randomPoints
    for country, xCoor, yCoor in zip(CountriesList, BirthRateList, LifeExpectancyList): 
        distancesToRandomPoints = [] 
        for number in randomPointGeneratorList: 
            distance = euc_distance(xCoor, BirthRateList[number], yCoor, LifeExpectancyList[number])
            distancesToRandomPoints.append(distance)
             
        minIndexValue = np.argmin(distancesToRandomPoints)
        firstClusterList[minIndexValue].append([country, xCoor, yCoor]) 
    
    # For debugging purposes, printing out the length of each cluster
    for i in range(len(firstClusterList)):
        print("Length of randomPoint cluster {}".format(i))
        print(len(firstClusterList[i]))
        
    '''
    Examples for the countries and their Birthrates / Life Expectancies: 
    The first number is the cluster number
    The second number refers to the position of the country in the cluster 
    The third number is the index for the country (0) Birthrate (1) and LifeExpectancy (2)
    '''

    '''
    firstClusterList: after the distances have been calculated they are clustered accordingly to the closest one (total length of 196 points)
    clusterMeanList: this list contains the means of the cluster points in firstClusterList (Length will be the amount of clusters (eg 10))
    distancesToMeanList: temporary storage of the distances to get the smallest one and cluster
    secondClusterList: here is where all the final clusters are stored accordingly  (total length of 196)
    
    '''
    # The iterations start here:  
    print("Calculating the mean and the distances to the means from each data point")
    # Calculating the mean for each cluster (BirthRate mean and LifeExpectancy Mean)
    for i in range (iterationInput):
        
        clusterMeanList = [[]for i in range(userInput)]
        
        for i in range(userInput):
            tempXList = []
            tempYList = []
            for j in (range(len(firstClusterList[i]))): 
                tempXList.append(firstClusterList[i][j][1])  # Birthrates
                tempYList.append(firstClusterList[i][j][2])  # LifeExpectancies
            
            meanX, meanY = mean (tempXList, tempYList)
            
            if math.isnan(meanX) and math.isnan(meanY):
                meanX = 0
                meanY = 0
            
            clusterMeanList[i].append([meanX, meanY])
            
        # print(clusterMeanList)
        secondClusterList = [[] for i in range(userInput)]

        # Calculating the EUC distance of points to the mean of the points
        squaredDistance = 0
        for countries, xCoor, yCoor in zip (CountriesList, BirthRateList, LifeExpectancyList): 
            distancesToMeansList = []
            
            for number in clusterMeanList: 
                distance = euc_distance(xCoor, number[0][0], yCoor, number[0][1])
                distancesToMeansList.append(distance)
                squaredDistance += np.square(distance)
            
            minValueIndex = np.argmin(distancesToMeansList)
            secondClusterList[minValueIndex].append([countries, xCoor, yCoor])
            
        firstClusterList = secondClusterList.copy()
        print("Squared Distances: converge to the following: {}".format(squaredDistance))
        # For debugging purposes, printing out the length of each cluster
        if (i == iterationInput): 
            break;
    
    print("Here are your clusters and the countries in each one: ")
    for i in range(len(secondClusterList)):
        print("Final cluster {}".format(i))
        
        for j in range(len(secondClusterList[i])):
            print(secondClusterList[i][j][0])
 
        # The iterations loop end here
        # Setting colors for the scatter plot, scatter plot will cycle through the colors as they print out 
    colors = itertools.cycle(['c', 'm', 'tab:gray', 'tab:pink', 'tab:purple', 'r', 'b', 'g', 'tan', 'teal', 'navy', 'blueviolet'])
        
        # Plotting out the secondCluster where the clusters have been arranged according to closest to mean
    for i in range(userInput):
        c = next(colors)
        for j in (range(len(secondClusterList[i]))): 
            plt.scatter(secondClusterList[i][j][1], secondClusterList[i][j][2], c=c)
            plt.scatter(clusterMeanList[i][0][0], clusterMeanList[i][0][1], c='black', marker=matplotlib.markers.CARETDOWNBASE)
            plt.title("Final clusters of countries")
            plt.xlabel("Birth rates per 1000")
            plt.ylabel("Life Expectancies")
            
    plt.show()  
    
    
# Main method 
if __name__ == "__main__": 
    Countries, BirthRates, LifeExpectancy = read()
    k_means(Countries, BirthRates, LifeExpectancy)
    
