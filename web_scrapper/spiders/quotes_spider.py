import re
from typing import List

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    scrape_list = ['xxxx']
    i = 0

    def start_requests(self):
        url = 'http://www.srilanka.travel/accommodation'
        # url = 'http://www.srilanka.travel/sitemap'
        yield scrapy.Request(url=url, callback=self.parse)


    def addPage(self,page):
        self.scrape_list.append(page)

    def getPages(self):
        return self.scrape_list

    def parse(self, response):
        page = response.url.split("/")[-1]
        if page == '':
            page = response.url
        page = re.sub(r'[/\\?%*:|"<>]', '', page)
        # self.i = self.i + 1
        # filename = 'pages/%s.html' % self.i

        filename = 'pages/%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        print('******************************************************************')


        next_page_list = response.css('a ::attr(href)').extract()
        if next_page_list is not None:
            for page in next_page_list:
                print(page)
                black_list = ['youtube','twitter', 'instagram', 'wikipedia', 'facebook', 'flickr', 'mailto', 'map.php', 'gov.lk', 'zimbra']
                scrape_list = self.getPages()
                if not any(substring in page for substring in black_list):
                    print("NOT BLACKLISTED")
                    if not any(substring in page for substring in scrape_list):
                        print("ADDING: "+page)
                        self.addPage(page)
                        if 'http' in page:
                            next_page = page
                        else:
                            next_page = response.urljoin(page)
                        yield scrapy.Request(next_page, callback=self.parse)
                    else:
                        print("ALREADY EXISTS: " + page)
                else:
                    print("BLACKLISTED!")
        print(self.getPages())
        print('22222222222222222222222222222222222222222')