import scrapy
from arxiv.items import ArxivItem

class ArxivphysicsSpider(scrapy.Spider):
    name = 'arxivphysics'
    allowed_domains = ['https://arxiv.org']
    base_urls = 'https://arxiv.org/list/physics/pastweek?skip='
    offset =0
    start_urls = [base_urls + str(offset)+ '&show=25']


    def parse(self, response):
        title_list = response.xpath('//div[@class="list-title mathjax"]/text()').extract()
        # abs_list = response.re('<a href="(/abs/.*)" title="Abstract">')
        abs_list = response.xpath("//span[@class='list-identifier']/a[@title='Abstract']/@href").extract()
        authors_list = response.xpath('//div[@class="list-authors"]/a/text()').extract()

        for i in zip(title_list, authors_list, abs_list):
            item = ArxivItem()
            item['title'] = i[0]
            item['authors'] = i[1]
            item['abstraction'] = i[2]

            yield item