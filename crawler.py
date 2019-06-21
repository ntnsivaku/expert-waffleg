import sys
import argparse
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as Soup
from urllib.parse import urlparse
from validator_collection import checkers
import urllib.error
import os


class WebCrawler():

	""" This class will crawl a URL and put all the crawled URLs 
		into a file or terminal output them """
		
	def __init__(self, url, max_depth, saveToFile ):

		self.soup = None					# Beautiful Soup object
		self.currentPage = url				# Current page's address
		self.links = set()					# Set to hold every unique links fetched
		self.maxdepth = max_depth			# stop crawling until max depth
		self.fileSaveStatus = saveToFile	# Save results to File?

	def crawl(self):
		'''Main function to crawl URL's '''

		''' opening up connection '''
		uClient = self.openUrl(self.currentPage)
		page_html = uClient.read()
		uClient.close()


		'''Fetch all links from the soup object'''
		self.soup = Soup(page_html, "lxml")

		page_links = []

		''' look for relative valid web-links one at a time 
			and append into list ''' 
		for link in [h.get('href') for h in self.soup.find_all('a')]:
			if link.startswith('http'):
				page_links.append(link)
			elif link.startswith('/'):
				parts = urlparse(self.currentPage)
				page_links.append(parts.scheme + '://' + parts.netloc + link)
			else:
				page_links.append(self.currentPage+link)

		self.links = set(page_links)

	def openUrl(self, url):
		''' Checks if URL is valid,
			and open the url using urlopen '''

		try:
			return uReq(url)
		except urllib.error.HTTPError as e:
			print(" **************** URL-Error exception raised **************** ")
			sys.exit(1)
		except urllib.error.URLError as e:
			print("**************** URL-Error exception raised **************** ")
			sys.exit(1)

	def writeToFile(self, url, page_list):
		'''Save output data in a file under current directory'''

		domain = urlparse(url)
		file_name = domain.netloc.split(".")[0]
		filepath = os.getcwd() + '/' + file_name + '.txt'
		with open(filepath, 'w') as file_handler:
			for item in page_list:
				file_handler.write("{}\n".format(item))

		print('Crawl done. Look for the output file at ', filepath)

	def run(self):
		''' Execute the crawl until the maximum depth specified
			and store the results in a file or print them to the console'''

		while len(self.links) < self.maxdepth:
			self.crawl()

		if not self.fileSaveStatus:
			for link in self.links:
				print(link)
		else:
			self.writeToFile(self.currentPage, self.links)


if __name__ == '__main__':
	''' define command line options
		this also generates --help and error handling '''

	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-u", 
		"--url",
		nargs="+",	# 1 or more values expected => creates a list
		dest = "url", 
		help="specify the url of the website/s to crawl eg:- https://github.com"
		)
	parser.add_argument(
		"-d", 
		"--depth",
		dest = "depth",
		type=int, 
		help="maximum depth to crawl"
		)
	parser.add_argument(
		"-f", 
		"--file",
		action='store_true',  
		help="Save output to file"
		)

	args = parser.parse_args()
	print( "url {} depth {} file {} ".format(
		args.url,
		args.depth,
		args.file
		))
	
	''' If depth specified use it as max_depth to crawl else
		set default depth to 3 '''
	if args.depth:
		depth = args.depth
	else:
		depth = 3

	''' Check if save to file option have been specified '''
	if args.file:
		saveStatus = True
	else:
		saveStatus = False

	''' Grab all the urls specified and start crawling one at a time''' 	
	try:
		for url in args.url:
			if checkers.is_url(url):
				C = WebCrawler(url, depth, saveStatus)
				C.run()
			else:
				print("**************** Invalid URL ****************")

	except KeyboardInterrupt:
		print("**************** Keyboard interrupt occured. Stopping the execution *******************")
		exit(0)
