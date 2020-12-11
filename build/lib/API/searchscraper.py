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


if __name__ == "__main__":

	# parse input arguments 
  	parser = argparse.ArgumentParser()
  	parser.add_argument('--search', nargs='+', type=str, default='None', help='enter the title or keyword to search')
  	parser.add_argument('--start', type=int, default=0, help='0 = most recent API result')
  	parser.add_argument('--max', type=int, default=10000, help='max paper bound')
  	parser.add_argument('--sort', type=str, default='relevance', help='can be "relevance", "lastUpdatedDate", "submittedDate"')
  	args = parser.parse_args()

  	search_query = "+".join(args.search)

  	query = 'search_query=%s&sortBy=%s&start=%i&max_results=%i' % (search_query,args.sort,args.start,args.max)

  	url = myBASE+query

  	response = urlopen(url)
  	xml = response.read()
  	root = ET.fromstring(xml)
  	records = root.findall(W3 + 'entry')

  	df_op = pd.DataFrame()

  	curr_time = datetime.now().strftime("%Y%m%d-%I%M%S")


  	for record in records:
  		meta = Record(record).__output__()
  		df_op = df_op.append(meta, ignore_index=True)


  	df_op.to_csv("results_"+curr_time+".csv", index=False)

