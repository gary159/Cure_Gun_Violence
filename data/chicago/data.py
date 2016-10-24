import pandas as pd
import numpy as np
import os
import argparse
from datetime import datetime
import numbers
import requests
import matplotlib.path as mplPath
import re


class ChicagoData():
	def __init__(self):
		self.CSV_FILE = "Crimes_-_2010_to_present.csv"
		self.df = pd.DataFrame()
		self.meta = dict()

	def read_data(self, limit=None):
		self.df = pd.read_csv(self.CSV_FILE, nrows=limit)
		return self	

	def read_meta(self):
		self.meta['community'] = self._read_community()
		self.meta['beat'] = self._read_beat()
		self.meta['district'] = self._read_district()
		self.meta['census'] = self._read_census()
		self.meta['fbi'] = self._read_fbi()

		
	def _read_community(self):
		community = pd.read_csv('community_areas.csv')
		return community

	def _read_beat(self):
		beat = pd.read_csv('police_beat.csv')
		return beat

	def _read_district(self):
		police_district = pd.read_csv('police_districts.csv')
		return police_district

	def _read_census(self):
		census = pd.read_csv('census_data.csv')
		return census

	def _read_fbi(self):
		fbi = pd.read_csv('fbi.csv')
		return fbi

	def pull_fbi_codes(self):
		url = "http://gis.chicagopolice.org/clearmap_crime_sums/crime_types.html"
		response = requests.get(url)
		content = response.content
		codes = re.findall("\r\n\t+.+<br>|\r\n\t+.+</td>", content)
		codes_clean = [re.sub('<td.*\"\d+\">|</[a-zA-Z]+>|<br>', "", c.replace("\r", "").replace("\t", "").replace("\n", "")) for c in codes]
		codes_split = [tuple(c.split(' ', 1)) for c in codes_clean if re.match("^\d", c)]
		pd.DataFrame(codes_split, columns=['CODE', 'DESCRIPTION']).to_csv('fbi.csv')
		return self

	def pull_data(self):
		os.system("curl 'https://data.cityofchicago.org/api/views/diig-85pa/rows.csv?accessType=DOWNLOAD' -o 'Crimes_-_2010_to_present.csv'")
		return self

	def merge_meta(self):
		self.df = self.df.merge(cd.meta['beat'], how='left', left_on='Beat', right_on='BEAT_NUM')
		self.df = self.df.merge(cd.meta['community'], how='left', left_on='Community Area', right_on='AREA_NUMBE')
		self.df = self.df.merge(cd.meta['census'], how='left', left_on='Community Area', right_on='Community Area Number')
		self.df = self.df.merge(cd.meta['fbi'], how='left', left_on='FBI CODE', right_on='CODE')
		return self

	def pull_metadata(self):
		os.system("curl 'https://data.cityofchicago.org/api/views/z8bn-74gv/rows.csv?accessType=DOWNLOAD' -o 'police_stations.csv'")
		os.system("curl 'https://data.cityofchicago.org/api/views/c7ck-438e/rows.csv?accessType=DOWNLOAD' -o 'IUCR.csv'")
		os.system("curl 'https://data.cityofchicago.org/api/views/n9it-hstw/rows.csv?accessType=DOWNLOAD' -o 'police_beat.csv'")
		os.system("curl 'https://data.cityofchicago.org/api/views/24zt-jpfn/rows.csv?accessType=DOWNLOAD' -o 'police_districts.csv'")
		os.system("curl 'https://data.cityofchicago.org/api/views/k9yb-bpqx/rows.csv?accessType=DOWNLOAD' -o 'wards.csv'")
		os.system("curl 'https://data.cityofchicago.org/api/views/igwz-8jzy/rows.csv?accessType=DOWNLOAD' -o 'community_areas.csv'")		
		os.system("curl 'https://data.cityofchicago.org/api/views/kn9c-c2s2/rows.csv?accessType=DOWNLOAD' -o 'census_data.csv'")
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
		pivot = counts.pivot('fields', 'Period', 'count')
		pivot_sort = pivot.sort_values(pivot.columns[-1], ascending=False)
		pivot_split = pivot_sort.reset_index().fields.str.split('---', expand=True).join(pivot_sort.reset_index(drop=True))
		pivot_rename = pivot_split.rename(columns={int(k): v for k, v in enumerate(fields)})
		return pivot_rename

	def check_borders(self, ID, dataset):
		point = self.df.loc[self.df.ID==ID, 'Location'].values[0]
			
		for index, row in self.meta[dataset].iterrows():
			coordinate_sets = re.match("MULTIPOLYGON \(\(\((.*)\)\)\)", row['the_geom']).group(1)
			coordinate_strings = [tuple(c.replace("\(", "").replace("\)", "").split(" ")) for c in coordinate_sets.split(", ")]
			coordinates = [(float(c[0]), float(c[1])) for c in coordinate_strings]
			bbPath = mplPath.Path(np.array(coordinates))
			
			if isinstance(point, basestring):
				point = point.replace("\(", "").replace("\)", "").replace(" ", "").split(", ")

			points = (float(point[0]), float(point[1]))

			if bbPath.contains_point(points):
				print 'index'
				return index


	def map_point(self, dataset):
		pass

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
	os.system('mkdir -p ./analysis')
	args = parse_args()
	cd = ChicagoData()
	
	if args.download_data:
		cd.pull_data()
	if args.download_metadata:
		cd.pull_metadata()	
		cd.pull_fbi_codes()

	cd.read_data(limit=args.limit)
	cd.read_meta()
	cd.merge_meta()
	

	print 'data:\n', cd.df
	for c in cd.df.columns:
		print c
	print 'min date: %s\nmax data: %s' % (cd.df['Date'].min(), cd.df['Date'].max())

	h = cd.hisotgram('Primary Type', dt_format='%m/%Y')
	print h
	if not args.limit:
		h.to_csv('./analysis/primary_description_stats.csv')
	
	d = cd.hisotgram(['Primary Type', 'Description'], dt_format='%m/%Y')
	print d
	if not args.limit:
		d.to_csv('./analysis/description_stats.csv')
	
	f = cd.hisotgram(['FBI Code'], dt_format='%m/%Y')
	print f
	if not args.limit:
		f.to_csv('./analysis/FBI_stats.csv')

	i = cd.hisotgram(['PER CAPITA INCOME'], dt_format='%Y')
	print i
	if not args.limit:
		i.to_csv('./analysis/income_stats.csv')

	hardship = cd.hisotgram(['PER CAPITA INCOME'], dt_format='%Y')
	print hardship
	if not args.limit:
		hardship.to_csv('./analysis/harship_stats.csv')


	corr = h.set_index('Primary Type').T.fillna(0).corr()
	if not args.limit:
		corr.to_csv('./analysis/primary_description_correlations.csv')


	for m in cd.meta:
		print m
		print cd.meta[m]

