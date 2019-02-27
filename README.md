# CCAPIformatter
Grabs hourly price data from Crypto Compare's API and formats it into comma-delimited .txt files for use with an ANN


Run CCApiHourlyPrice to create a .txt file called "results", containing hourly data of BTC/USDT pricing on binance. 
Each row of data in "results" will be in this format: timestamp for that hour, close price for that hour, hourly high, and hourly low. 
An open price is not needed as it will be identical to the close price of the previous hour.

After running CCApiHourlyPrice, run close4hourFormatter. This will read through results.txt and produce another .txt file. 
In this file, there will be comma separated lines of the following format:
timestamp for the hour of interest (TOI), A, B, C
Where A, B, and C are:
  A:  1 if the hourly high for one hour before the TOI is equal to or greater than 1% above the starting price for that hour
      -1 if the hourly hight for one hour before TOI is less than -1% relative to the starting price for that hour
      0 otherwise
  B:  like A, but instead of one hour before TOI, it is two hours before TOI
  C:  like A, but instead of one hour before TOI, it is three hours before TOI
  
The output of close4hourFormatter can be changed via some simple alerations to produce whatever dataset you want. The datea is meant to be used in an Artificial Nueral Network. The ANN code may be published here but it is someone else's modified code, so I am awaiting their consent before publishing.
