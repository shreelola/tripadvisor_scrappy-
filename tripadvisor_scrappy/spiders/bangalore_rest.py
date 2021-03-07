import scrapy
import os

class BangaloreRestSpider(scrapy.Spider):
    name = 'bangalore-rest'
    allowed_domains = ['www.tripadvisor.in/Search?q=bangalore+restaurants']
    start_urls = ['https://www.tripadvisor.in/Search?q=bangalore+restaurants/']

    def parse(self, response):
        rest_list = response.css('div[class="_1kXteagE"]')
        links = []
        print(rest_list)
        for test in rest_list:
            print(test)
            link_test = test.xpath('//a/@href').extract()
            links.extend(link_test)
            print("Debug 1 %s", type(link_test))
            # yield {
            #       'links':  link_test
            # }



        # print(links)
        link_list = []
        for link in set(links):
            full_link = os.path.join("https://www.tripadvisor.in/", link)
            # if link.startswith('/ShowUserReviews'):
            print(("https://www.tripadvisor.in" + link))

        # print(link_list)
