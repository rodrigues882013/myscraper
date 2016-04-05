import logging
import requests
import os
import sys

from bs4 import BeautifulSoup
from PIL import Image


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
		logger.info("Start receiving an url to parse")
		self.url = url

	def open_url(self):
		logger.info("Open the url received")
		logger.info("Working")

		self.page = requests.get(self.url)
		logger.info("End")

	def build_soup_objects(self):
		logger.info("Creating a soup object")
		logger.info("Working")

		html_doc = self.page.text
		self.soup = BeautifulSoup(html_doc, 'html.parser')
		logger.info("End")

	def save_images(self):
		logger.info("Saving images on AWS3")
		logger.info("Working")

		image_tags = [img for img in self.soup.findAll('img')]
		logger.debug("Images: %s", str(image_tags))
		
		image_links = [img.get('src') for img in image_tags]
		logger.debug("\nImage links: %s", str(image_links))

		for link in image_links:
			image = requests.get("http:" + link)
			
		
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
	s.save_images()


if __name__ == '__main__':
	main()
	