import scrapy
from urllib.parse import urlencode

API_key = 'ace1d4a22b164f3694148566b57fe2ba'

def get_proxy_url(url):
    country = "IN"
    payload = {
        'url' : url,
        'x-api-key' : API_KEY,
        'proxy_country' : country,
        'browser' : 'false'
    }
    proxy_url = "https://api.scrapingant.com/v2/general?" + urlencode(payload)
    return proxy_url


class ScarpeLaptopsSpider(scrapy.Spider):
    name = "scarpe_laptops"
    allowed_domains = ["www.flipkart.com"]
    start_urls = ["https://www.flipkart.com/computers/laptops/pr?sid=6bo,b5g&otracker=categorytree"]

    def parse(self, response):
        products = response
