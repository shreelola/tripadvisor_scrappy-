# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorScrappyItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    date = scrapy.Field()
    hotel_name = scrapy.Field()
    location = scrapy.Field()
    review = scrapy.Field()
