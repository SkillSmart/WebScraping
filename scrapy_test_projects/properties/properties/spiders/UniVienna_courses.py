# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from properties.items import DegreeItem, CourseItem
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
    name = 'UniVienna_courses'
    start_urls = ['http://studentpoint.univie.ac.at/studies/alle-studien/?no_cache=1']

    def parse(self, response):
        """ This function will parse vertically trough all available courses at the University of Vienna'
        @scrapes course_title stammdaten studienaufbau studienziel berufsfelder
        @scrapes url project spider server date
        """
        # Extract subpage urls and create full url paths
        degree_selector = response.xpath('//a[contains(@class, "studium")]//@href')
        
        # Parse each Detailed Course Page and create a 'Degree Entry'
        for url in degree_selector.extract():
            yield Request(urljoin(response.url, url), callback=self.parse_courses)


    def parse_courses(self, response):
        course = CourseItem()
        # Iterate over each table on the Page (Holding information about a degree module)
        for section in response.xpath('//table[@class="table-head-top"]'):
            # Set up a dict to store the course informationf for this degree module
            # Parse
            section_title = section.xpath('.//th[@class="firstcol"]/text()').re_first(r'\w+')

            # Iterate over all courses(rows) and get [coursename, ects] and store them on the 
            for module in section.xpath('.//tr'):
                
                course['university'] = 'University Vienna'
                course['degree'] = response.xpath('//div[@class="inner"]/h1/text()').extract()
                course['course_title'] = module.xpath('.//td[@class="firstcol"]/text()').extract()
                course['course_module'] = section_title
                course['course_ects'] = module.xpath('.//td[@class="lastcol"]').re_first(r'\d+')
                yield course
