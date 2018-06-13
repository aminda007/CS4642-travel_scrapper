from typing import List

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
            'http://www.srilanka.travel/sitemap'
        ]

    scrape_list=['xxxx']

    def addPage(self,page):
        self.scrape_list.append(page)

    def getPages(self):
        return self.scrape_list

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        print('******************************************************************')


        next_page_list = response.css('li a::attr(href)').extract()
        if next_page_list is not None:
            for page in next_page_list:
                print(page)
                black_list = ['youtube','twitter', 'instagram', 'wikipedia', 'facebook']
                scrape_list = self.getPages()
                for bl in black_list:
                    if bl not in page:
                        print("NOT BLACKLISTED")
                        for sl in scrape_list:
                            if sl not in page:
                                print("ADDING: "+page)
                                self.addPage(page)
                                next_page = response.urljoin(page)
                                yield scrapy.Request(next_page, callback=self.parse)
                            else:
                                print("ALREADY EXISTS: " + page)
                    else:
                        print("BLACKLISTED!")