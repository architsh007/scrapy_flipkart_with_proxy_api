from urllib import response
import scrapy
from urllib.parse import urlencode
from selectolax.parser import HTMLParser  


class ScrapeLaptopsSpider(scrapy.Spider):
    name = "scrape_laptops"
    allowed_domains = ["www.flipkart.com"]
    start_urls = ["https://www.flipkart.com/computers/laptops/pr?sid=6bo,b5g&otracker=categorytree"]

    
    def get_proxy_url(self, url):
        """
        It takes url and convert it to the proxy url (scrapingant) for the request the required url
        """
        API_KEY = 'ace1d4a22b164f3694148566b57fe2ba'
        country = "IN"
        payload = {
            'url' : url,
            'x-api-key' : API_KEY,
            'proxy_country' : country,
            'browser' : 'false'
        }
        proxy_url = "https://api.scrapingant.com/v2/general?" + urlencode(payload)
        return proxy_url


    def extract_text(self, selector, text_deep = True, text_strip = False):
        """
        It takes the css selector and converts the output to text if that tag is present and return None type if its is not present
        """
        try:
            return selector.text(deep = text_deep, strip = text_strip)
        except AttributeError:
            return None
        

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(self.get_proxy_url(url), callback=self.parse)


    def parse(self, response):
        #Converting the repsonse to the selectolax praser
        html = HTMLParser(response.text)
