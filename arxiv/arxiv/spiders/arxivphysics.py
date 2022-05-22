from encodings import utf_8
import scrapy
from arxiv.items import ArxivItem

class ArxivphysicsSpider(scrapy.Spider):
    name = 'arxivphysics'
    allowed_domains = ['arxiv.org']

    base_urls = 'https://arxiv.org'
    list_urls = '/list/physics/pastweek?skip='
    offset = 0
    start_urls = [base_urls + list_urls + str(offset)+ '&show=25']


    def parse(self, response):
        title_list = response.xpath('//div[@class="list-title mathjax"]/text()[2]').extract()
        # abs_list = response.re('<a href="(/abs/.*)" title="Abstract">')
        abs_list = response.xpath("//span[@class='list-identifier']/a[@title='Abstract']/@href").extract()
        # authors_list = response.xpath('//div[@class="list-authors"]/a/text()').extract()
        # print(f'{title_list=}')
        # for i in zip(title_list, abs_list):
            # item = ArxivItem()
            # item['title'] = i[0]
            # item['authors'] = i[1]
            # item['abstraction'] = i[2]
        for i in zip(title_list, abs_list):
            abs_url = self.base_urls + i[1]
            # print(f'{i[0].strip()=}')
            # yield item
            yield scrapy.Request(url=abs_url, callback=self.parse_abstr, meta={'title': i[0].strip()})
        self.offset += 25
        next_url = self.base_urls + self.list_urls + str(self.offset)+ '&show=25'
        yield scrapy.Request(url=next_url, callback=self.parse)

    # To parse the abstrction from link
    def parse_abstr(self, response):
        authors_list = response.xpath('//div[@class="authors"]/a/text()[1]').extract()
        abstr_content = response.xpath('//blockquote/text()[2]').extract()
        download_link = response.xpath('//a[@class="abs-button download-pdf"]/@href[1]').extract()
        # for i in zip(authors_list, abstr_content):
        #     item = ArxivItem()
        #     item['title'] = response.meta['title']
        #     item['authors'] = i[0]
        #     item['abstraction'] = i[1]
        #     yield item
        item = ArxivItem()
        item['title'] = response.meta['title']
        item['authors'] = authors_list
        item['abstraction'] = abstr_content[0]
        item['download'] = self.base_urls + download_link[0]
        # print(item)
        yield item