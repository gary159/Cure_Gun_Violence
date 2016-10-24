import pandas as pd
import numpy as np
import os
import argparse
from datetime import datetime
import numbers
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

	def pull_data(self):
		os.system("curl 'https://data.cityofchicago.org/api/views/diig-85pa/rows.csv?accessType=DOWNLOAD' -o 'Crimes_-_2010_to_present.csv'")
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

	def check_borders(self, point, dataset):
		coordinate_sets = re.match("MULTIPOLYGON \(\(\((.*)\)\)\)", self.meta[dataset].ix[0]['the_geom']).group(1)
		coordinate_strings = [tuple(c.split(" ")) for c in coordinate_sets.split(", ")]
		coordinates = [(float(c[0]), float(c[1])) for c in coordinate_strings]
		bbPath = mplPath.Path(np.array(coordinates))
		if isinstance(point, basestring):
			point_set = point.strip('\(').strip('\)').strip(" ").split(',')

		points = (float(point_set[0]), float(point_set[1]))

		return bbPath.contains_point(points)

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

	cd.read_data(limit=args.limit)
	cd.read_meta()

	data = cd.df
	print 'data:\n', data
	for c in data.columns:
		print c
	print 'min date: %s\nmax data: %s' % (data['Date'].min(), data['Date'].max())

	h = cd.hisotgram('Primary Type', dt_format='%m/%Y')
	print h
	if not args.limit:
		h.to_csv('./analysis/primary_description_stats.csv')
	
	d = cd.hisotgram(['Primary Type', 'Description'], dt_format='%m/%Y')
	print d
	if not args.limit:
		d.to_csv('./analysis/description_stats.csv')
	
	corr = h.set_index('Primary Type').T.fillna(0).corr()
	if not args.limit:
		corr.to_csv('./analysis/primary_description_correlations.csv')


	for m in cd.meta:
		print m
		print cd.meta[m]

	print cd.check_borders(data.ix[0]['Location'], 'beat')