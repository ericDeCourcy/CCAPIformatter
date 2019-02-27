#this program takes in data outputted from CCApiHourlyPrice.py and formats it like so...
#first column is change in close price since last hour
#second column is change in close price from two hours ago to one hour ago
#third column is change in close price from three hours ago to two hours ago
#fourth column a 1 iff high price in next hour is >= 2% what the close price is
	#else, its a zero
#if there's not enough data to do anything with (less than 2 previous times, or at final time there's nothing to say about next hour), just put N/A for whole row

fIn = open("results.txt", "r")
fOut = open("close1pcHighLowResults.txt", "a")

#num entries to read
numEntries = 10000
numPreviousHours = 3 #don't just change this... more work needs to be done to change the number of previous hours used

#put a header at the top indicating the first timestamp found and the pair, just for posterity
#uses a pound sign to delimit beginning of data
fOut.write("---- BTC/USDT on binance, starting at 1512133200 ----\n#\n")

contents = fIn.read()

#indexes for placing data in dictionary 
CLOSE = 1
HIGH = 2

#create a dictionary of close vals and high vals mapped to timestamps
closeAndHigh = {}

firstTs = 0

for x in range(1,numEntries + 1):
	#find index of comma at end of timestamp
	tsEndIndex1 = str(contents).index(",")

	#find value of timestamp
	tsVal1 = int(str(contents)[0:tsEndIndex1])
	#print(tsVal1)

	if x is 1:
		firstTs = tsVal1

	#create new string containing anything past first ts
	contentsPastTS1 = str(contents)[tsEndIndex1+1:]

	#find index of next comma
	closeEndIndex1 = str(contentsPastTS1).index(",")

	#find value of close for hour 1
	close1Val = float(str(contentsPastTS1)[:closeEndIndex1])
	#print(close1Val)

	#create string of everything past close1
	contentsPastC1 = str(contentsPastTS1)[closeEndIndex1+1:]

	#find high value end index
	highEndIndex1 = str(contentsPastC1).index(",")

	#find value of high for hour 1
	high1Val = float(str(contentsPastC1)[:highEndIndex1])
	#print(high1Val)

	#put close and high vals into a dictionary
	closeAndHigh[tsVal1,CLOSE] = close1Val
	closeAndHigh[tsVal1,HIGH] = high1Val

	if x < numEntries:
		#find index of nextTs
		ts2Index = str(contents).index(str(tsVal1 + 3600))
		#print(ts2Index)
		
		#erase line one of original contents
		contents = str(contents)[ts2Index:]

	if (x%100) is 0:
		print(x)

for y in range(0, numEntries):
	
	currentTs = firstTs + y*3600

	if y > numPreviousHours:
		
		oneHourAgo = currentTs - 3600
		twoHoursAgo = currentTs - 7200
		threeHoursAgo = currentTs - 10800
		fourHoursAgo = currentTs - 14400
		
		#find change of one hour ago, two hours ago, three hours ago
		oneHourChange = 100*(closeAndHigh[oneHourAgo,CLOSE] - closeAndHigh[twoHoursAgo,CLOSE])/closeAndHigh[twoHoursAgo,CLOSE]
		twoHourChange = 100*(closeAndHigh[twoHoursAgo,CLOSE] - closeAndHigh[threeHoursAgo,CLOSE])/closeAndHigh[threeHoursAgo,CLOSE]
		threeHourChange = 100*(closeAndHigh[threeHoursAgo,CLOSE] - closeAndHigh[fourHoursAgo,CLOSE])/closeAndHigh[fourHoursAgo,CLOSE]

		#find high percentage happening in this hour
		highPercentage = 100*(closeAndHigh[currentTs,CLOSE] - closeAndHigh[oneHourAgo,CLOSE])/closeAndHigh[oneHourAgo,CLOSE]

		if highPercentage > 0.999999:
			fOut.write(str(currentTs) + "," + str(oneHourChange) + "," + str(twoHourChange) + "," + str(threeHourChange) + "," + "1,\n")
		elif highPercentage < -0.99999:
			fOut.write(str(currentTs) + "," + str(oneHourChange) + "," + str(twoHourChange) + "," + str(threeHourChange) + "," + "-1,\n")
		else:
			fOut.write(str(currentTs) + "," + str(oneHourChange) + "," + str(twoHourChange) + "," + str(threeHourChange) + "," + "0,\n")


	else:
		fOut.write(str(currentTs) + "," + "N/A,\n")

	if (y%100) is 0:
		print(y)
	

fIn.close()
fOut.close()
