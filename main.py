import logging
import requests
import os
import sys

from bs4 import BeautifulSoup


logger = logging.getLogger('SuitsSupply WebScraper')
logger.setLevel(logging.DEBUG)

fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(fmt)
console_handler.setLevel(logging.DEBUG)

logger.addHandler(console_handler)


class SuitsSupplyScraper(object):
	url = None
	page = None
	soup = None

	def __init__(self, url):
		logger.info("Start receiving a url to parse")
		self.url = url

	def open_url(self):
		logger.info("Open url")
		logger.info("Working")
		self.page = requests.get(self.url)
		logger.info("End")

	def build_soup_objects(self):
		logger.info("Creating a soup object")
		logger.info("Working")
		self.soup = BeautifulSoup(self.page.text)
		logger.info("End")

	def save_images(self):
		logger.info("Saving images on AWS3")
		logger.info("Working")
		logger.info("End")
		
	def save_videos(self):
		logger.info("Saving videos on AWS3")
		logger.info("Working")
		logger.info("End")
		
	def save_documents(self):
		logger.info("Saving documents on AWS3")
		logger.info("Working")
		logger.info("End")
		
		

def main():
	url = sys.argv[1]

	s = SuitsSupplyScraper(url)
	s.open_url()
	s.build_soup_objects()


if __name__ == '__main__':
	main()
	