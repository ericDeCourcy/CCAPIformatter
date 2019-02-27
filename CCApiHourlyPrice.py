import urllib.request

f = open("results.txt", "a")

#add &toTs=x to get all data up to the timestamp x
#this command will return last 2000 samples
contents = urllib.request.urlopen("https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USDT&e=binance&limit=2000").read()

finalSample = 1548133200	#this is the final timestamp for now. This corresponds to roughly midnight on 1/22/19
numSampleSets = 5	#number of sets of "entriesPerSample" samples
entriesPerSample = 2000 #number of samples per call (2000 is max)

samplingIntervalTS = entriesPerSample*3600	#this is the number of seconds in each sampleSet


for sampleCall in range(1,numSampleSets+1):
	timeToCall = finalSample - samplingIntervalTS*(numSampleSets - sampleCall)
	print(str(numSampleSets - (sampleCall)))

	contents = urllib.request.urlopen("https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USDT&e=binance&limit=2000&toTs=" + str(timeToCall)).read()

	#get hourly close, low, and high
	#the close of one hour is the same as the open of the next hour, so we only need one
	for x in range(1, entriesPerSample+1):
		timeIndex = str(contents).index("time")	#finds the index of the first letter of the first occurrence of "time" in "contents"
		closeIndex = str(contents).index("close")
		highIndex = str(contents).index("high")
		lowIndex = str(contents).index("low")
		openIndex = str(contents).index("open")

		time = str(contents)[timeIndex+6:closeIndex-2]
		close = str(contents)[closeIndex+7:highIndex-2]
		high = str(contents)[highIndex+6:lowIndex-2]
		low = str(contents)[lowIndex+5:openIndex-2]

		with open("testSet_200.txt", "a") as f:
			f.write(time + "," + close + "," + high + "," + low + "," + "\n")
		
		#print(time + "," + close + "," + high + "," + low + ",")

		contents = str(contents)[openIndex+1:]



#save all that data into a csv file
f.close()

