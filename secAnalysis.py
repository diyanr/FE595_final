import matplotlib.pyplot as plt 
import csv
import numpy as np
import pandas as pd

# Read data
def getData():
	readData =  pd.read_csv("Data/results.csv")
	data = readData[readData.Sentiment != 0]
	return data

# Plots average sentiment over 10 years vs average yearly returns over 10 years
def averageSentimentvsReturns():
	data = getData()
	avgSent = []
	avgReturns = []
	setInd = 0
	sentiSum = 0
	returns = 0
	for index, row in data.iterrows():
		sentiSum += data["Sentiment"][index]
		returns += (data["Q1"][index] + data["Q2"][index] + data["Q3"][index] + data["Q4"][index])
		
		if (setInd == 10):
			setInd = 0
			avgSent.append(sentiSum/10)
			avgReturns.append(returns/40)
			sentiSum = 0
			returns = 0
		else:
			setInd += 1

	fig, ax = plt.subplots()
	ax.scatter(avgReturns, avgSent)
	ax.set_title("Average Sentiment vs Average Yearly Returns")
	ax.set_xlabel("Average Yearly Returns")
	ax.set_ylabel("Average Sentiment")
	plt.show()

def averageChangevsSentiment():
	data = getData()
	avgChange = []
	avgSent = []
	sentiSum = 0
	changeSum = 0
	setInd = 0
	for index, row in data.iterrows():
		sentiSum += data["Sentiment"][index]
		changeSum += ((data["Q4"][index] - data["Q1"][index]) / 3)
		if (setInd == 10):
			setInd = 0
			avgSent.append(sentiSum/10)
			avgChange.append(changeSum/10)
			sentiSum = 0
			changeSum = 0
		else:
			setInd += 1
	fig, ax = plt.subplots()
	ax.scatter(avgChange, avgSent)
	ax.set_title("Average Sentiment vs Average Change per Quarter")
	ax.set_xlabel("Average Change per Quarter")
	ax.set_ylabel("Average Sentiment")
	plt.show()



averageSentimentvsReturns() 
averageChangevsSentiment()
