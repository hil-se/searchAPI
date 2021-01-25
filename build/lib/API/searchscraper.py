import os
import time
import pickle
import random
import argparse
import feedparser
import xml.etree.ElementTree as ET
from datetime import datetime
import sys
import pandas as pd

import urllib.request
import urllib.parse
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError

W3 = '{http://www.w3.org/2005/Atom}'
A9 = '{http://a9.com/-/spec/opensearch/1.1/}'
myBASE = 'http://export.arxiv.org/api/query?'


class Record(object):

	def __init__(self, xml_file):
		self.xml = xml_file
		self.id = self.__to_text__(W3, 'id')
		self.summary = self.__to_text__(W3, 'summary')
		self.title = self.__to_text__(W3, 'title')
		self.author = self.__get_authors__()
		self.updated = self.__get_year__()

	def __to_text__(self, namespace, tag):
		try:
			return self.xml.find(namespace + tag).text.strip().lower().replace('\n','.')
		except:
			return ''

	def __get_name__(self, parent, attribute):
	    try:
	    	return parent.find(W3 + attribute).text.lower()
	    except:
	    	return "n/a"

	def __get_authors__(self):
		authors_xml = self.xml.findall(W3 + 'author')
		names = [self.__get_name__(author, 'name') for author in authors_xml]
		return names

	def __get_year__(self):
	    updated_year = self.__to_text__(W3, 'updated')
	    year = updated_year[0:4]
	    return year

	def __output__(self):
		dict = {'PDF Link' : self.id,
				'Abstract' : self.summary,
				'Document Title' : self.title,
				'Author' : self.author,
				'Year': self.updated}
		return dict

class Scraper(object):
	def __init__(self, search_query=None, start=0, max_results=10, sortBy='relevance'):
		self.search_query = str(search_query)
		# self.id_list = str(id_list)
		self.start = start
		self.max_results = max_results
		# self.url = get_url(search_query, id_list, start, max_results, sortBy, sortOrder)
		self.search_query = "+".join(self.search_query)
		self.query = 'search_query=%s&sortBy=%s&start=%i&max_results=%i' % (self.search_query,self.sortBy,self.start,self.max_results)
		self.url = myBASE + self.query

	def __scrape__(self):
		t0 = time.time()
		tx = time.time()
		elapsed = 0.0
		url = self.url
		df_op = pd.DataFrame(columns=("PDF Link", "Abstract", "Document Title","Author","Year"))
		curr_time = datetime.now().strftime("%Y%m%d-%I%M%S")
		k = 1
		while True:

			print('fetching up to ', 1000 * k, 'records...')
			try:
				response = urlopen(url)
			except HTTPError as e:
				if e.code == 503:
					tp = int(e.hdrs.get('retry-after', 30))
					print('Got 503. Retrying after {0:d} seconds.'.format(self.t))
					time.sleep(self.t)
					continue
				else:
					raise

			k += 1
			xml = response.read()
			root = ET.fromstring(xml)
			records = root.findall(W3 + 'entry')

		  	# df_op = pd.DataFrame()



			for record in records:
				meta = Record(record).__output__()
				df_op = df_op.append(meta, ignore_index=True)



			ty = time.time()
			elapsed += (ty-tx)
			if elapsed >= self.timeout:
				break
			else:
				tx = time.time()

		t1 = time.time()
	  	
		print('fetching is completed in {0:.1f} seconds.'.format(t1 - t0))
		print ('Total number of records {:d}'.format(len(ds)))	  	

		df_op.to_csv("results_"+curr_time+".csv", index=False)

		return df_op



	def __get_url__(search_query, id_list, start, max_results, sortBy, sortOrder):
		query_list = [search_query, id_list, start, max_results, sortBy, sortOrder]
		filter_query = []
		filter_query = find_None(query_list)
		url_methodName =""


	def __find_None__(query_list):
		filter_list = []
		for query in query_list:
			if query is not None:
				filter_list.append(query)

		return filter_list


# if __name__ == "__main__":

# 	# parse input arguments 
#   	parser = argparse.ArgumentParser()
#   	parser.add_argument('--search', nargs='+', type=str, default='None', help='enter the title or keyword to search')
#   	parser.add_argument('--start', type=int, default=0, help='0 = most recent API result')
#   	parser.add_argument('--max', type=int, default=10000, help='max paper bound')
#   	parser.add_argument('--sort', type=str, default='relevance', help='can be "relevance", "lastUpdatedDate", "submittedDate"')
#   	args = parser.parse_args()

#   	search_query = "+".join(args.search)

#   	query = 'search_query=%s&sortBy=%s&start=%i&max_results=%i' % (search_query,args.sort,args.start,args.max)

#   	url = myBASE+query

#   	response = urlopen(url)
#   	xml = response.read()
#   	root = ET.fromstring(xml)
#   	records = root.findall(W3 + 'entry')

#   	df_op = pd.DataFrame()

#   	curr_time = datetime.now().strftime("%Y%m%d-%I%M%S")


#   	for record in records:
#   		meta = Record(record).__output__()
#   		df_op = df_op.append(meta, ignore_index=True)


#   	df_op.to_csv("results_"+curr_time+".csv", index=False)

