import pandas as pd
import numpy as np
import os
import argparse
from datetime import datetime
import numbers
import requests
import matplotlib.path as mplPath
import re
from sklearn.linear_model import LinearRegression
from statsmodels.api import OLS


class ChicagoData():
	def __init__(self):
		self.DATA_PATH =  os.path.join(os.path.dirname(__file__), "data/")
		self.CSV_FILE = self.DATA_PATH + "Crimes_-_2010_to_present.csv"
		self.df = pd.DataFrame()
		self.meta = dict()
		self.gun_fbi_codes = ['01A', '2', '3', '04B', '04A', '15']

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
		community = pd.read_csv(self.DATA_PATH + 'community_areas.csv')
		return community

	def _read_beat(self):
		beat = pd.read_csv(self.DATA_PATH + 'police_beat.csv')
		return beat

	def _read_district(self):
		police_district = pd.read_csv(self.DATA_PATH + 'police_districts.csv')
		return police_district

	def _read_census(self):
		census = pd.read_csv(self.DATA_PATH + 'census_data.csv')
		return census[~np.isnan(census['Community Area Number'])]

	def _read_fbi(self):
		fbi = pd.read_csv(self.DATA_PATH + 'fbi.csv')
		return fbi

	def pull_fbi_codes(self):
		url = "http://gis.chicagopolice.org/clearmap_crime_sums/crime_types.html"
		response = requests.get(url)
		content = response.content
		codes = re.findall("\r\n\t+.+<br>|\r\n\t+.+</td>", content)
		regex = '.*</span><span class="crimetype"><a href="#.*">(.+).*\((.+)\)</a>.*'
		special_codes = [re.match(regex, c.replace(' (Index)', '').replace("\r", "").replace("\t", "").replace("\n", "")).groups() for c in codes if '</span><span class="crimetype"><a href=' in c]
		special_codes_ordered = [(c[1], c[0]) for c in special_codes]
		codes_clean = [re.sub('<td.*\"\d+\">|</[a-zA-Z]+>|<br>', "", c.replace("\r", "").replace("\t", "").replace("\n", "")) for c in codes]
		codes_split = [tuple(c.split(' ', 1)) for c in codes_clean if re.match("^\d", c)]
		pd.DataFrame(codes_split+special_codes_ordered, columns=['CODE', 'FBI DESCRIPTION']).to_csv(self.DATA_PATH + 'fbi.csv')
		return self

	def pull_data(self):
		os.system("curl 'https://data.cityofchicago.org/api/views/diig-85pa/rows.csv?accessType=DOWNLOAD' -o '%sCrimes_-_2010_to_present.csv'" % self.DATA_PATH)
		return self

	def merge_meta(self):
		self.df = self.df.merge(cd.meta['beat'], how='left', left_on='Beat', right_on='BEAT_NUM', suffixes=('', '_beat'))
		self.df = self.df.merge(cd.meta['community'], how='left', left_on='Community Area', right_on='AREA_NUMBE', suffixes=('', '_community'))
		self.df = self.df.merge(cd.meta['census'], how='left', left_on='Community Area', right_on='Community Area Number')
		self.df = self.df.merge(cd.meta['fbi'], how='left', left_on='FBI Code', right_on='CODE')
		return self

	def pull_metadata(self):
		os.system("curl 'https://data.cityofchicago.org/api/views/z8bn-74gv/rows.csv?accessType=DOWNLOAD' -o '%spolice_stations.csv'" % self.DATA_PATH)
		os.system("curl 'https://data.cityofchicago.org/api/views/c7ck-438e/rows.csv?accessType=DOWNLOAD' -o '%sIUCR.csv'" % self.DATA_PATH)
		os.system("curl 'https://data.cityofchicago.org/api/views/n9it-hstw/rows.csv?accessType=DOWNLOAD' -o '%spolice_beat.csv'" % self.DATA_PATH)
		os.system("curl 'https://data.cityofchicago.org/api/views/24zt-jpfn/rows.csv?accessType=DOWNLOAD' -o '%spolice_districts.csv'" % self.DATA_PATH)
		os.system("curl 'https://data.cityofchicago.org/api/views/k9yb-bpqx/rows.csv?accessType=DOWNLOAD' -o '%swards.csv'" % self.DATA_PATH)
		os.system("curl 'https://data.cityofchicago.org/api/views/igwz-8jzy/rows.csv?accessType=DOWNLOAD' -o '%scommunity_areas.csv'" % self.DATA_PATH)		
		os.system("curl 'https://data.cityofchicago.org/api/views/kn9c-c2s2/rows.csv?accessType=DOWNLOAD' -o '%scensus_data.csv'" % self.DATA_PATH)
		return self


	def community_crimes(self):
		comm = self.pivot(['Community Area', 'the_geom_community'], '%Y')
		print comm.the_geom_community.ix[1]

	def _parse_geom(self):
		pass


	def pivot(self, fields, dt_format, metric=None):
		use_metric=True
		if not isinstance(fields, list):
			if isinstance(fields, (basestring, numbers.Integral)):
				fields = [fields]
			else:
				fields = list(fields)

		if not metric:
			use_metric = False
			metric = 'Period'
			self.df[metric] = self.df['Date'].map(lambda x: datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p').strftime(dt_format))

		counts = self.df.groupby([metric]+fields, as_index=False).count().iloc[:, 0:len(fields)+2] 
		counts.columns = [metric]+fields+['count']
		for i, f in enumerate(fields):
			if i==0:
				counts['fields'] = counts[f].map(lambda x: str(x))
			else:
				counts['fields'] +='---'+counts[f].map(lambda x: str(x))
		pivot = counts.pivot('fields', metric, 'count')
		pivot_sort = pivot.sort_values(pivot.columns[-1], ascending=False)
		pivot_split = pivot_sort.reset_index().fields.str.split('---', expand=True)
		pivot_rename = pivot_split.rename(columns={int(k): v for k, v in enumerate(fields)})
		pivot_join = pivot_rename.merge(pivot_sort.reset_index(drop=True), left_index=True, right_index=True)
		if use_metric:
			return pivot_join.set_index(fields).T.reset_index()
		else:
			return pivot_join



	def regression(self):
		data = self.df
		data_filtered = data[data['Primary Type']=='WEAPONS VIOLATION']
		c = list(self.meta['census'].columns)
		c.remove('Community Area Number')
		c.remove('COMMUNITY AREA NAME')
		c.append('COMMUNITY')
		c.append('SHAPE_AREA')
		c.append('Location Description')
		c.append('Year')
		data_mat = data_filtered[c+['Primary Type']].groupby(c, as_index=False).count()
		
		year =pd.get_dummies(data_mat['Year'])
		loc =pd.get_dummies(data_mat['Location Description'])
		community =pd.get_dummies(data_mat['COMMUNITY'])

		mat = data_mat.join(year).join(loc).join(community).drop('Year', axis=1).drop('Location Description', axis=1).drop('COMMUNITY', axis=1)
		X = mat[[c for c in mat.columns if c!='Primary Type']]
		y = mat['Primary Type']
		
		significant_cols = list()

		print '----------INDIVIDUAL REGRESSION----------'
		for c in X:
			print c
			result = self._model(X[c], y)
			significant_cols += list(result.pvalues[result.pvalues<0.05].axes[0])

		print '----------TOTAL REGRESSIONION----------'
		result = self._model(X, y)

		result = self._model(X[significant_cols], y)
		

	def _model(self, X, y):
		model = OLS(y, X)
		result = model.fit()
		print result.summary()
		return result

	def analysis(self, args):
		os.system('mkdir -p ./analysis')
	
		gun_fbi_codes = self.gun_fbi_codes


		print 'data:\n', self.df
		for c in self.df.columns:
			print c
		print 'min date: %s\nmax data: %s' % (self.df['Date'].min(), self.df['Date'].max())

		h = self.pivot('Primary Type', dt_format='%m/%Y')
		print h
		if not args.limit:
			h.to_csv('./analysis/primary_description_stats.csv')
		
		d = self.pivot(['Primary Type', 'Description'], dt_format='%m/%Y')
		print d
		if not args.limit:
			d.to_csv('./analysis/description_stats.csv')
		
		f = self.pivot(['FBI DESCRIPTION'], dt_format='%m/%Y')
		print f
		if not args.limit:
			f.to_csv('./analysis/FBI_stats.csv')

		
		lf = self.pivot(['Location Description', 'FBI DESCRIPTION'], dt_format='%Y')
		print lf
		if not args.limit:
			lf.to_csv('./analysis/locationtype_FBI_stats.csv')

		lp = self.pivot(['Location Description', 'Primary Type'], dt_format='%Y')
		print lp
		if not args.limit:
			lp.to_csv('./analysis/locationtype_primary_stats.csv')

	 	corr = h.set_index('Primary Type').T.fillna(0).corr()
		if not args.limit:
			corr.to_csv('./analysis/primary_description_correlations.csv')

		income = self.pivot(['FBI DESCRIPTION', 'FBI Code'], dt_format='%m/%Y', metric='PER CAPITA INCOME ')
		print 'income\n', income
		if not args.limit:
			income.to_csv('./analysis/income_FBI_stats.csv')


		print self.meta['census']
		harship = self.pivot(['FBI DESCRIPTION', 'FBI Code'], dt_format='%m/%Y', metric='HARDSHIP INDEX')
		print 'harship\n', hardshp
		if not args.limit:
			harship.to_csv('./analysis/hardship_FBI_stats.csv')

		
		self.regression()


def parse_args():
	parser = argparse.ArgumentParser(description="Chicago_Data")
												
	parser.add_argument("-download_data",  action="store_true",
						help="use to download csv data file")

	parser.add_argument("-download_metadata",  action="store_true",
						help="use to download csv meta data files")
	
	parser.add_argument("-download_fbi",  action="store_true",
						help="pull and parse fbi code data to csv")
												
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
	if args.download_fbi:
		cd.pull_fbi_codes()

	cd.read_data(limit=args.limit)
	cd.read_meta()
	cd.merge_meta()
	cd.community_crimes()

	for c in cd.df.columns:
		print c
	