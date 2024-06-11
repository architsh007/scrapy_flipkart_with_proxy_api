import scrapy
from urllib.parse import urlencode
from selectolax.parser import HTMLParser




class ScarpeLaptopsSpider(scrapy.Spider):
    name = "scarpe_laptops"    

    def get_proxy_url(self, link):
        API_KEY = 'ace1d4a22b164f3694148566b57fe2ba'
        country = "IN"
        payload = {
            'url' : link,
            'x-api-key' : API_KEY,
            'proxy_country' : country,
            'browser' : 'false'
        }
        proxy_url = "https://api.scrapingant.com/v2/general?" + urlencode(payload)
        return proxy_url


    def start_requests(self):
        start_urls = ["https://www.flipkart.com/computers/laptops/pr?sid=6bo,b5g&otracker=categorytree"]
        for link in start_urls:
            yield scrapy.Request(self.get_proxy_url(link), self.parse)
    
    def parse(self, response):
        resp = response.text
        html = HTMLParser(resp)
        
        products = html.css('a.CGtC98')

        def extract_text(selector, text_deep = True, text_strip = False):
            """
            Enter the css selector tag from text has to be extracted and return the text if present or return None when it is not present in that tag
            deep argumnet in text is enabled by default and strip is disabled until it will be enabled by user
            """
            try:
                return selector.text(deep = text_deep, strip = text_strip)
            except AttributeError:
                return None
        
        def extract_product_details(product):
            details = []
            for detail in product.css('li'):
                details.append(extract_text(detail))
            return details
        
        def extract_no_rating(product):
            string = extract_text(product.css_first('span.Wphh3N'))
            if string is not None:
                string = str(string)
                no_of_rating = string.split(sep="&")[0]
                return no_of_rating.strip()
            else:
                return None
            
        def extract_no_reviews(product):
            string = extract_text(product.css_first('span.Wphh3N'))
            if string is not None:
                string = str(string)
                no_of_reviews = string.split(sep="&")[1]
                return no_of_reviews.strip()
            else:
                return None


        for product in products:
            yield{
                'name' : extract_text(product.css_first('div.KzDlHZ')),
                'specification' : extract_product_details(product),
                'selling_price' : extract_text(product.css_first('div.Nx9bqj._4b5DiR')),
                'MRP' : extract_text(product.css_first('div.yRaY8j.ZYYwLA')),
                'ratings' : extract_text(product.css_first('div.XQDdHH')),
                'no_of_ratings' : extract_no_rating(product),
                'no_of_reviews' : extract_no_reviews(product)
            }
