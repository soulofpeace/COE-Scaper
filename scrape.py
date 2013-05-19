from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from StringIO import StringIO
import pyPdf
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdevice import PDFDevice, TagExtractor

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
        #pdf = pyPdf.PdfFileReader(StringIO(response.body))
        laparams = LAParams()
        outtype = 'text'
        codec = 'utf-8'
        caching = True
        srcmgr = PDFResourceManager(caching=caching)
        outfp = StringIO()
        maxpages = 0
        password = ''
        rsrcmgr = PDFResourceManager(caching=caching)
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
        process_pdf(rsrcmgr, device, StringIO(response.body), set(), maxpages=maxpages, password=password,
                                    caching=caching, check_extractable=True)

        #content=""
        #for page in pdf.pages:
            #content += page.extractText() + "\n"
        #content = " ".join(content.replace(u"\xa0", " ").strip().split()) 
        print outfp.getvalue()
