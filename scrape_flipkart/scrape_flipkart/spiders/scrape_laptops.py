from urllib import response
import scrapy
from urllib.parse import urlencode, urljoin
from selectolax.parser import HTMLParser
from scrape_flipkart.items import ScrapeFlipkartItem  


class ScrapeLaptopsSpider(scrapy.Spider):
    name = "scrape_laptops"
    allowed_domains = ["www.flipkart.com", "api.scrapingant.com"]
    start_urls = ["https://www.flipkart.com/computers/laptops/pr?sid=6bo%2Cb5g&otracker=categorytree&page=1"]

    custom_settings = {
            'FEEDS': { 'data.jsonl': { 'format': 'jsonlines', 'overwrite' : True}},
        }

    
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


    def extract_details(self, html):
        """
        This function extract all detailed specification that are present in the product element in form of list 
        """
        details = []
        for detail in html.css('li'):
            details.append(self.extract_text(detail, text_strip=True))
        return details
    
    
    def check_class(self, html, element):
        """
        Checks whether selected element is present in the that html
        """
        try:
            while html.css_matches(element):
                return True
        except AttributeError:
            return False
        
    
    def extract_no_rating(self, product):
        string = self.extract_text(product.css_first('span.Wphh3N'))
        if string is not None:
            string = str(string)
            no_of_rating = string.split(sep="&")[0]
            return no_of_rating.strip()
        else:
            return None
        

    def extract_no_reviews(self, product):
        string = self.extract_text(product.css_first('span.Wphh3N'))
        if string is not None:
            string = str(string)
            no_of_reviews = string.split(sep="&")[1]
            return no_of_reviews.strip()
        else:
            return None


    def parse(self, response):
        #Converting the repsonse to the selectolax praser
        html = HTMLParser(response.text)

        #Select all the laptop element tags from the page
        products = html.css('a.CGtC98')
        laptop = ScrapeFlipkartItem()
        
        for product in products:
            laptop['name'] = self.extract_text(product.css_first('div.KzDlHZ'))
            laptop['selling_price'] = self.extract_text(product.css_first('div.Nx9bqj._4b5DiR'), text_strip=True)
            laptop['max_retail_price'] = self.extract_text(product.css_first('div.yRaY8j.ZYYwLA'), text_strip=True)
            laptop['specifications'] = self.extract_details(product)
            laptop['free_delivery'] = self.check_class(product, 'div.yiggsN')
            laptop['off_percentage'] = self.extract_text(product.css_first('.UkUFwK'))
            laptop['f_assured'] = self.check_class(product, '.UkUFwK')
            laptop['rating'] = self.extract_text(product.css_first('.XQDdHH'))
            laptop['no_of_ratings'] = self.extract_no_rating(product)
            laptop['no_of_reviews'] = self.extract_no_reviews(product)
            laptop['url'] = urljoin(self.start_urls[0], product.css_first('a.CGtC98').attrs['href']) # type: ignore
            yield laptop

        for _ in list(html.css('a._9QVEpD')): # type: ignore
            if str.lower(_.text(strip=True)) == 'next':
                next_page_url = urljoin(self.start_urls[0], _.css_first('a._9QVEpD').attrs['href']) # type: ignore

                if next_page_url is not None:
                    yield scrapy.Request(self.get_proxy_url(next_page_url), callback = self.parse)
