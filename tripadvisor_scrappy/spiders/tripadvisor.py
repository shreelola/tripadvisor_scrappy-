import scrapy
from tripadvisor_scrappy.items import TripadvisorScrappyItem
from scrapy import Request


class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    start_urls = ['https://www.tripadvisor.in/Search?q=bangalore+restaurants/']

    def parse(self, response):
        rest_list = response.css('div[data-test-target="restaurants-list"]')
        for test in rest_list:
            link_test = test.xpath('//a/@href').extract()

            for link in set(link_test):
                if link.startswith('/Restaurant_Review'):
                    test_Link = "https://www.tripadvisor.in" + link
                    url_detail = response.urljoin(test_Link)
                    print(url_detail)
                    yield Request(url=url_detail, callback=self.parse_detail)

        next_page = response.xpath('//div[@class="unified pagination js_pageLinks"]/a/@href').extract()
        if next_page:
            url = "https://www.tripadvisor.in" + next_page[-1]
            url_next_page = response.urljoin(url)
            yield Request(url_next_page, self.parse)

    def parse_detail(self, response):
        # Page with hotel's description
        # Loop for 5 reviews per page, request link within 'Next' button
        hotel_name = response.xpath("//h1[@data-test-target ='top-info-header']/text()").get()
        reviews = response.xpath("//div[@class='review-container']")
        item = TripadvisorScrappyItem()
        item['hotel_name'] = hotel_name
        item['location'] = "bangalore"
        for review in range(len(reviews)):
            item['title'] = reviews[review].xpath(".//span[@class='noQuotes']/text()").get()

            rev_bub = ''
            if reviews[review].xpath(".//span[@class='ui_bubble_rating bubble_50']"): rev_bub = '5'
            if reviews[review].xpath(".//span[@class='ui_bubble_rating bubble_45']"): rev_bub = '4,5'
            if reviews[review].xpath(".//span[@class='ui_bubble_rating bubble_40']"): rev_bub = '4'
            if reviews[review].xpath(".//span[@class='ui_bubble_rating bubble_35']"): rev_bub = '3,5'
            if reviews[review].xpath(".//span[@class='ui_bubble_rating bubble_30']"): rev_bub = '3'
            if reviews[review].xpath(".//span[@class='ui_bubble_rating bubble_25']"): rev_bub = '2,5'
            if reviews[review].xpath(".//span[@class='ui_bubble_rating bubble_20']"): rev_bub = '2'
            if reviews[review].xpath(".//span[@class='ui_bubble_rating bubble_15']"): rev_bub = '1,5'
            if reviews[review].xpath(".//span[@class='ui_bubble_rating bubble_10']"): rev_bub = '1'
            if reviews[review].xpath(".//span[@class='ui_bubble_rating bubble_05']"): rev_bub = '0,5'
            if reviews[review].xpath(".//span[@class='ui_bubble_rating bubble_00']"): rev_bub = '0'

            item['rating'] = rev_bub

            item['date'] = reviews[review].xpath(".//span[@class='ratingDate']/@title").extract()[0]
            item['review'] = reviews[review].xpath(".//p[@class='partial_entry']/text()").get().replace("\n", " ")

            # Request page of particular review, call parse_review method

        btn_next = response.xpath("//link[@rel='next']/@href").extract()[0]
        url_next = 'https://www.tripadvisor.in' + btn_next
        if btn_next:
            yield Request(url=url_next, callback=self.parse_detail)

        yield item
