import pandas as pd
import sys,csv,requests,os
from bs4 import BeautifulSoup

def RequestandMake(symbol, path, Call = True):
	res = requests.get("https://www.marketwatch.com/investing/index/" +symbol+"/options?countrycode=US&showAll=True")
	soup = BeautifulSoup(res.content,'lxml')
	table = soup.find_all('table')[0]
	df = pd.read_html(str(table))

	#print(tabulate(df, headers='keys', tablefmt='psql'))
	headr = ['Symbol', 'Last', 'Change', 'Vol', 'Bid', 'Ask', 'Open','Strike']
	
	#Call only
	if Call == True:
		Calls = df[0][3:].drop(df[0].columns[8:],axis = 1)
		Calls.columns = headr
		#	Remove Puts_only
		Calls = Calls[Calls['Last'] != 'quote']
	
		#Set columns to Symbol,Bid,Strike
		dropcol = [0,2,3,4,6,7]
		Calls.drop(Calls.columns[dropcol],axis = 1,inplace = True)
		ExpDatesDF = pd.DataFrame(data = Calls['Symbol'][Calls['Symbol'].str.contains("Expires") == True])
		ExpDates = []
		for i in ExpDates['Symbol']: 
			ExpDates.append(i[8:])
		for index, row in ExpDatesDF.iterrows():
			index
		
		#make csv
		os.makedirs(path+'/'+symbol)
		Calls.to_csv(path+'/'+symbol+'/'+symbol+'.csv')
		
	#df[0][3:].to_csv(cwd+'/'+symbol +'.csv')

	return;

cwd = os.getcwd()

if sys.argv[1] == '-r':

	for x in sys.argv[2:]:
		RequestandMake(x,cwd)
		print (x)
if sys.argv[1] == 'SP500':
	sp = '/home/tamezarnold/Data/SP500.txt'
	path = '/home/tamezarnold/Data/MarketWatch'
	reader = open(sp,"r")

	for line in reader:
        	symbol =  line.strip("\n")
        	try:
			RequestandMake(symbol,path)
        	except:
          	 	 print "error reading " + symbol
	reader.close()
