# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeFlipkartItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    selling_price = scrapy.Field()
    max_retail_price = scrapy.Field()
    specifications = scrapy.Field()
    free_delivery = scrapy.Field()
    off_percentage = scrapy.Field()
    f_assured = scrapy.Field()
    rating = scrapy.Field()
    no_of_ratings = scrapy.Field()
    no_of_reviews = scrapy.Field()
    url = scrapy.Field()
