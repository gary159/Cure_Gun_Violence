import pandas as pd
import os
import argparse
from datetime import datetime
import numbers

class ChicagoData():
	def __init__(self):
		self.CSV_FILE = "Crimes_-_2010_to_present.csv"

	def read_data(self, limit=None):
		self.df = pd.read_csv(self.CSV_FILE, nrows=limit)
		return self		

	def pull_data(self):
		os.system("curl 'https://data.cityofchicago.org/api/views/diig-85pa/rows.csv?accessType=DOWNLOAD' -o 'Crimes_-_2010_to_present.csv'")
		return self

	def pull_metadata(self):
		os.system("curl 'https://data.cityofchicago.org/api/views/z8bn-74gv/rows.csv?accessType=DOWNLOAD' -o 'police_stations.csv'")
		os.system("curl 'https://data.cityofchicago.org/api/views/c7ck-438e/rows.csv?accessType=DOWNLOAD' -o 'IUCR.csv'")
		os.system("curl 'https://data.cityofchicago.org/api/views/n9it-hstw/rows.csv?accessType=DOWNLOAD' -o 'police_beat.csv'")
		os.system("curl 'https://data.cityofchicago.org/api/views/24zt-jpfn/rows.csv?accessType=DOWNLOAD' -o 'police_districts.csv'")
		os.system("curl 'https://data.cityofchicago.org/api/views/k9yb-bpqx/rows.csv?accessType=DOWNLOAD' -o 'wards.csv'")
		os.system("curl 'https://data.cityofchicago.org/api/views/igwz-8jzy/rows.csv?accessType=DOWNLOAD' -o 'community_ares.csv'")		
		os.system("curel 'https://data.cityofchicago.org/api/views/kn9c-c2s2/rows.csv?accessType=DOWNLOAD' -o 'census_data.csv'")
		return self

	def hisotgram(self, fields, dt_format):
		if not isinstance(fields, list):
			if isinstance(fields, (basestring, numbers.Integral)):
				fields = [fields]
			else:
				fields = list(fields)

		self.df['Period'] = self.df['Date'].map(lambda x: datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p').strftime(dt_format))
		counts = self.df.groupby(['Period']+fields, as_index=False).count().iloc[:, 0:len(fields)+2] 
		counts.columns = ['Period']+fields+['count']
		
		for i, f in enumerate(fields):
			if i==0:
				counts['fields'] = counts[f]
			else:
				counts['fields'] +='---'+counts[f]
		pivot = counts.pivot('fields', 'Period', 'count').sort_values(2016, ascending=False)
		pivot = pivot.reset_index().fields.str.split('---', expand=True).join(pivot.reset_index(drop=True))
		pivot = pivot.rename(columns={int(k): v for k, v in enumerate(fields)})
		return pivot

def parse_args():
	parser = argparse.ArgumentParser(description="Chicago_Data")
												
	parser.add_argument("-download_data",  action="store_true",
						help="use to download csv data file")

	parser.add_argument("-download_metadata",  action="store_true",
						help="use to download csv meta data files")
												
	parser.add_argument("-limit",  metavar='limit', type = int, default=None,
                            help="limit size of data for faster testing of code")


	args = parser.parse_args()
	return args



if __name__=="__main__":
	args = parse_args()
	cd = ChicagoData()
	if args.download_data:
		cd.pull_data()
	if args.download_metadata:
		cd.pull_metadata()	
	cd.read_data(limit=args.limit)
	
	data = cd.df
	print 'data:\n', data
	for c in data.columns:
		print c
	h = cd.hisotgram('Primary Type', dt_format='%Y%m')
	os.system('mkdir -p ./analysis')
	h.to_csv('./analysis/primary_description_stats.csv')
	print h
	d = cd.hisotgram(['Primary Type', 'Description'], dt_format='%Y%m')
	d.to_csv('./analysis/description_stats.csv')
	print d[d['Primary Type']=='WEAPONS VIOLATION']
