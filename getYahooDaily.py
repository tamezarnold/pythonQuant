from datetime import datetime
import requests, json
import pandas as pd

today = datetime.datetime.now()
today_fmtd = today.strftime('%Y-%m-%d')

sp = '~/Data/SP500.txt'
header = ['Date','Open','High','Low','Close','Adj Close','Volume','Pct Change']

reader = open(sp,"r")

def options_reader(stock):
	url0 = 'https://query1.finance.yahoo.com/v7/finance/options/'+stock
	
	try:re = requests.get(url0)
	except:
		print('Ivalid request')
		return 0
	jd = json.loads(re.text)
	options = jd['optionChain']['result'][0]['options'][0]
	exp_date = datetime.fromtimestamp(options['expirationDate'])
	
	df_calls = pd.DataFrame(options['calls'])
	df_calls['expirationDate'] = exp_date

	df_puts = pd.DataFrame(options['puts'])
	df_puts['expirationDate']=exp_date
	
	return {'puts':df_puts,'calls':df_calls}
		
def daily_reader(stock):
	#retieve webpage
	url = YAHOO+'quote/'+stock+'/history?p='+stock
	re = requests.get(url)

	##pd.read_html looks for 'table' but yahoo didn't label the table
	try:df=pd.read_html(re.text.replace('tbody','table'))[1]
	except:
		#print('Unable to read html')
		return 0
	#add the header
	df.columns=header[:-1]
	
	#some rows have dividends
	df.replace(to_replace=r'. Dividend$',value=np.nan,regex=True,inplace=True)
	df.dropna(inplace=True)
	
	#set the dataframe index to be the date column
	df.set_index('Date',inplace=True)
	df.index=pd.to_datetime(df.index,dayfirst=True)
	df.sort_index(inplace=True)
	
	#include PCT_CHANGE
	df['Pct Change']=df['Adj Close'].astype('float').pct_change()
	return df

for line in reader:
	stock =  line.strip("\n")
	file_name = '~/Data/Yahoo/
	try:
		daily_reader(stock).to_csv(file_name+'Daily/'+ stock + '.csv')
		options = options_reader(stock)
		options['calls'].to_csv(file_name+f'options/{today_fmtd}_{stock}_calls.csv')
		options['puts'].to_csv(file_name+f'options/{today_fmtd}_{stock}_puts.csv')
	except:
		print "error reading " + stock
reader.close()
