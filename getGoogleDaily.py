from pandas.io.data  import DataReader
from datetime import datetime
import sys


sp = 'SP500.txt'

reader = open(sp,"r")

for line in reader:
	stock =  line.strip("\n")
	data  = DataReader(stock,  'google', datetime(2010, 1, 1), datetime(2017, 1, 1))
	file_name = '~/Data/DailyfromGoogle/'+ stock + '.csv'
	data.to_csv(file_name)

reader.close()
