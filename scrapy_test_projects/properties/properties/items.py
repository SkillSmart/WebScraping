# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class PropertiesItem(scrapy.Item):
    # Primary Fields
    course_title = Field()
    stammdaten = Field()
    studienziel = Field()
    studienaufbau = Field()
    berufsfelder = Field()

    # Calculated Fields
    location = Field()

    # Housekeeping Fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()
