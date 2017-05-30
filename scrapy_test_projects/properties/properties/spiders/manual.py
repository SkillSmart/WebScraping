# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from properties.items import PropertiesItem
# Class to attribute the parsed Data to a variable
from scrapy.loader import ItemLoader
# Classes for Preprocessing the Data
from scrapy.loader.processors import MapCompose, Join



# General imports
import re
import datetime
import socket
from urllib.parse import urlparse
from urllib.parse import urljoin


class BasicSpider(scrapy.Spider):
    name = 'manual'
    start_urls = ['http://studentpoint.univie.ac.at/studies/alle-studien/?no_cache=1']

    def parse(self, response):
        """ This function will parse vertically trough all available courses at the University of Vienna'
        @scrapes course_title stammdaten studienaufbau studienziel berufsfelder
        @scrapes url project spider server date
        
        """
        # Extract subpage urls and create full url paths
        degree_selector = response.xpath('//a[contains(@class, "studium")]//@href')
        
        for url in degree_selector.extract():
            yield Request(urljoin(response.url, url), callback=self.parse_degree)

    def parse_degree(self, response):
        # Instantiate the ItemClass to store the values
        item = PropertiesItem()
        # Assign the crawled values
        item['course_title'] = response.xpath('//div[@class="inner"]/h1/text()').extract()
        item['stammdaten'] = response.xpath('//div[@class="stammdaten"]').extract()
        item['studienaufbau'] = response.xpath('//div[@class="content"]')[1].extract()
        item['studienziel'] = response.xpath('//div[@class="content"]')[0].extract()
        item['berufsfelder'] = response.xpath('//div[@class="content"]')[2].extract()
        
        # Extracting the detailed Study Program
        degree_strct = {}
        # Extract all Degree Modules from the Page (contain module information)
        section = response.xpath('//table[@class="table-head-top"').extract()
        for module in section:
            # Collect Header information
            section_title = module.xpath('.//th[@class="firstcol"]/text()').re_first(r'\w+')
            module_courses = module.xpath('//tbody/tr/td[@class="firstcol"]/text()')
            module_ects = module.xpath('.//tbody/tr/td[@class="lastcol"]/text()').re_first(r'\d+')

            # Join Header info and then split into two parts (TODO: Insert Regex parsing here to extract clean information)
            mod_title = re.match("^\w*", module_header)
            mod_ects = re.match("(\d*)\sECTS", module_header)
        


        # Add Log Information (Housekeeping)
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

        return item