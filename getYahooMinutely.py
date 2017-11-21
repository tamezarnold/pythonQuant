from pandas_datareader import data as dreader
from datetime import datetime

sp = '/home/tamezarnold/Data/SP500.txt'

reader = open(sp,"r")

for line in reader:
	stock =  line.strip("\n")
	file_name = '~/Data/Yahoo/Daily/'+ stock + '.csv'
	try:
		dreader.DataReader(stock,  'yahoo', datetime(2000, 1, 1), datetime(2017, 1, 1)).to_csv(file_name)
	except:
		print "error reading " + stock
reader.close()