import subprocess
from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request

class COESpider(BaseSpider):
    name='coe'
    allowed_domains = ['www.lta.gov.sg']
    start_urls = [
            'http://www.lta.gov.sg/content/ltaweb/en/publications-and-research.html'
            ]

    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)
        print response
        hxs = HtmlXPathSelector(response)
        for link in hxs.select('//a[contains(@href, "COE_Result")]/@href').extract():
            yield Request('http://www.lta.gov.sg'+link, callback=self.parse_pdf)

    def parse_pdf(self, response):
        self.log('pdf %s response' % response.url)
        filename_tokens = response.url.split("/")
        filename = filename_tokens[len(filename_tokens)-1]
        with open("pdfs/{0}".format(filename), 'wb') as f:
            f.write(response.body)

        subprocess.call("ruby pdf_parser.rb pdfs/{0}".format(filename), shell=True)


