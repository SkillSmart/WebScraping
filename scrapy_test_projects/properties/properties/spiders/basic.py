# -*- coding: utf-8 -*-
import scrapy
from properties.items import PropertiesItem
# Class to attribute the parsed Data to a variable
from scrapy.loader import ItemLoader
# Classes for Preprocessing the Data
from scrapy.loader.processors import MapCompose, Join


# General imports
import datetime
import socket
from urllib.parse import urlparse
from urllib.parse import urljoin


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['web']
    start_urls = ['http://studentpoint.univie.ac.at/studies/detailansicht/studium/033-697/?tx_univiestudentpoint_pi1%5Bbackpid%5D=96352&cHash=f758a8d2abf36f5eeff223b0c854bdb2']

    def parse(self, response):
        """ This function parses the 'University Vienna Degree Detail Pages for all types of degrees.'
        @scrapes course_title stammdaten studienaufbau studienziel berufsfelder
        @scrapes url project spider server date
        
        """
        item = PropertiesItem()
        item['course_title'] = response.xpath('//div[@class="inner"]/h1/text()').extract()
        item['stammdaten'] = response.xpath('//div[@class="stammdaten"]').extract()
        item['studienaufbau'] = response.xpath('//div[@class="content"]')[1].extract()
        item['studienziel'] = response.xpath('//div[@class="content"]')[0].extract()
        item['berufsfelder'] = response.xpath('//div[@class="content"]')[2].extract()
        
        # Housekeeping
        item['url'] = response.url
        item['project'] = self.settings.get('BOT_NAME')
        item['spider'] = self.name
        item['server'] = socket.gethostname()
        item['date'] = datetime.datetime.now()

        # Adding manually created values 'housekeeping' to the Itemloader
        # l.add_value('url', response.url)
        # l.add_value('project', self.settings.get('BOT_NAME'))
        # l.add_value('spider', self.name)
        # l.add_value('server', socket.gethostname())
        # l.add_value('date', datetime.datetime.now())

        # 
        return item