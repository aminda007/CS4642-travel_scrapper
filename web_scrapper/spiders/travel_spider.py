import re
from typing import List

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "travel"

    scrape_list = ['xxxx']
    i = 0

    def start_requests(self):
        urls = [
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=4&hotel_district=&hotel_star=5',
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=4&hotel_district=&hotel_star=unclassified',
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=1&hotel_district=',
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=2&hotel_district=',
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=3&hotel_district=&hotel_grade=',
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=5&hotel_district=&hotel_grade=',
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=6&hotel_district=&hotel_grade=',
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=7&hotel_district=&hotel_grade=',
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=9&hotel_district=&hotel_grade=',
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=10&hotel_district=&hotel_grade=',
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=11&hotel_district=&hotel_grade=',
            'http://www.srilanka.travel/index.php?route=travel/tostay&hotel_type=19&hotel_district='
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def addPage(self,page):
        self.scrape_list.append(page)

    def getPages(self):
        return self.scrape_list

    def parse(self, response):
        pages = response.url.split("/")[-1]
        if pages == '':
            pages = response.url
        pages = re.sub(r'[/\\?%*:|"<>]', '', pages)
        # self.i = self.i + 1
        # filename = 'pages/%s.html' % self.i

        filename = 'pages/travel/%s.html' % pages
        with open(filename, 'wb') as f:
            f.write(response.body)
        print('******************************************************************')

        for quote in response.css('div.travel-hotel-inner'):
            name = quote.css('div.travel-hotel.row div.hname.span6 h4::text').extract_first()
            category = quote.css('div.travel-hotel.row div.hname.span6 div.row div.span5 p span::text').extract_first()
            capacity = quote.css('div.travel-hotel.row div.hname.span6 div.row div.span1 p span::text').extract_first()
            address = quote.css('div.travel-hotel.row div.hname.span6 div.row div.address.span6 p span::text').extract_first()
            website = quote.css('div.travel-hotel.row div.hname.span6 div.row div.span5 p span a::text').extract_first()
            phone_number = quote.css('div.travel-hotel.row div.hname.span6 div.row div.span5 p span::text').extract()[1]
        yield {
            'Name': name,
            'Category': category,
            'Capacity': capacity,
            'Address': address,
            'Phone_Number': phone_number,
            'Website': website,
            # 'Capacity': quote.css('::text').extract_first(),
        }

        next_page_list = response.css('div.links a ::attr(href)').extract()
        if next_page_list is not None:
            for page in next_page_list:
                print(page)
                black_list = ['youtube', 'twitter', 'instagram', 'wikipedia', 'facebook', 'flickr', 'mailto', 'map.php', 'gov.lk', 'zimbra']
                scrape_list = self.getPages()
                if not any(substring in page for substring in black_list):
                    # print("NOT BLACKLISTED")
                    if not any(substring in page for substring in scrape_list):
                        # print("ADDING: "+page)
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
        # print(self.getPages())
        # print('22222222222222222222222222222222222222222')