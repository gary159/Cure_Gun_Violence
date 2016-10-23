import pandas as pd
import os
import argparse
from datetime import datetime


class ChicagoData():
	def __init__(self):
		self.CSV_FILE = "Crimes_-_2010_to_present.csv"

	def read_data(self):
		self.df = pd.read_csv(self.CSV_FILE)
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
		return self

	def hisotgram(self, field):
		self.df['Year'] = self.df['Date'].map(lambda x: datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p').year)
		return self.df.groupby(['Year', field], as_index=False).count() #.sort_values('count', ascending=False)

	def timeline(self):
		pass


def parse_args():
	parser = argparse.ArgumentParser(description="Chicago_Data")
												
	parser.add_argument("-download_data",  action="store_true",
						help="use to download csv data file")

	parser.add_argument("-download_metadata",  action="store_true",
						help="use to download csv meta data files")
												
	args = parser.parse_args()
	return args



if __name__=="__main__":
	args = parse_args()
	cd = ChicagoData()
	if args.download_data:
		cd.pull_data()
	if args.download_metadata:
		cd.pull_metadata()
	cd.read_data()
	data = cd.df
	print 'data:\n', data
	for c in data.columns:
		print c
	print cd.hisotgram('Primary Type')