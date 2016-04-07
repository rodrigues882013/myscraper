import logging
import requests
import os
import sys
import boto

from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO


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
	out = None
	conn = None
	bucket = None
	

	def __init__(self, url):
		logger.info("Start receiving an url to parse")
		self.url = url

		logger.info("Connecting on Amazon S3")
		self.conn = boto.connect_s3()

		logger.info("Creating a bucket")
		self.bucket = self.conn.create_bucket('as3_suistsuply_test')

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

	def open_images(self):
		logger.info("Saving images on AWS3")
		logger.info("Working")

		image_tags = [img for img in self.soup.findAll('img')]		
		image_links = [img.get('src') for img in image_tags]
		image_bytes = [requests.get("http:" + link) for link in image_links]
		self.out = [dict(content=Image.open(StringIO(img.content)), 
			type=img.headers['Content-type'].split('/')[1]) for img in image_bytes]

		logger.info("End")
			
	def open_videos(self):
		logger.info("Saving videos on AWS3")
		logger.info("Working")
		logger.info("End")
		
	def open_documents(self):
		logger.info("Saving documents on AWS3")
		logger.info("Working")

		doc_tags = [doc for doc in self.soup.findAll('a')]		
		document_links = [doc.get('href') for doc in documments_tags]
		document_bytes = [requests.get("http:" + link) for link in document_links]
		self.out = [dict(content=StringIO(doc.content)), 
			type=doc.headers['Content-type'].split('/')[1]) for doc in document_bytes]

		logger.info("End")

	def push_items_on_s3(self):

		cont = 0
		for f in self.out:
			aux = StringIO()
			f['content'].save(aux, f['type'].upper())

			#Creating a key
			logger.info("Creating a key")
			key = self.bucket.new_key('file-{0}.{1}'.format(cont, f['type']))

			#Setting the key content
			logger.info("Setting a key content")
			key.set_contents_from_string(aux.getvalue())

			#Set the access control list (ACL)
			logger.info('Making the ACL public')
			key.set_acl('public-read')
			cont+=1
		
	

def proccess(s):

	try:
		logger.info("Proccessing operations.")
		s.open_url()
		s.build_soup_objects()
		s.open_images()
		s.push_items_on_s3()

		return True

	except Exception as e:
		logger.error(e)



def main():
	url = sys.argv[1]
	logger.debug("URL given: %s", url)

	obj = SuitsSupplyScraper(url)
	proccess(obj)

	


if __name__ == '__main__':
	main()
	