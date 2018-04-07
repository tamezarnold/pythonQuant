import pandas as pd
import requests,os
from bs4 import BeautifulSoup
from datetime import datetime

class getBloomberg(object):
	def __init__(self):
		self.sources = ['stocks','currencies','commodities','rates-bonds']
		self.timestamp = datetime.now()
		self.cwd = os.getcwd()
		self.outfile = str(datetime.now().month) +'_'+str(datetime.now().day)+'.txt'
	def set_outfile(self, outfile):
		self.outfile = outfile
	def get(self,source):
		res = requests.get("https://www.bloomberg.com/markets/"+source)
		soup = BeautifulSoup(res.content,'lxml')
		table = soup.find_all('table')
		data = pd.read_html(str(table))
		return data
	def allsources(self):
		outfile = self.outfile
		sources = self.sources
		file = open(outfile,'a+')
		for source in sources:
			try:
				data = self.get(source)
				file.write(source+ '\n')
				file.write(str(data).replace(',','\n').replace(']','\n'))
			except:
				print('could not open '+ source)
		print('done')
		file.close()
