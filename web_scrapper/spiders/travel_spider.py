import re
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "travel"

    scrape_list = ['xxxx']
    name_array = []
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

    def addName(self,name):
        self.name_array.append(name)

    def getNames(self):
        return self.name_array

    def parse(self, response):

        # scrape_list = self.getPages()
        # page_url = response.url
        # self.addPage(page_url)
        # if not any(substring in page_url for substring in scrape_list):
        # pages = response.url.split("/")[-1]
        # if pages == '':
        #     pages = response.url
        # pages = re.sub(r'[/\\?%*:|"<>]', '', pages)
        # self.i = self.i + 1
        # filename = 'pages/%s.html' % self.i

        # filename = 'pages/travel/%s.html' % pages
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # print('******************************************************************')

        for quote in response.css('div.travel-hotel-inner'):
            name = quote.css('div.travel-hotel.row div.hname.span6 h4::text').extract_first()
            category = quote.css('div.travel-hotel.row div.hname.span6 div.row div.span5 p span::text').extract_first()
            capacity = quote.css('div.travel-hotel.row div.hname.span6 div.row div.span1 p span::text').extract_first()
            address = quote.css('div.travel-hotel.row div.hname.span6 div.row div.address.span6 p span::text').extract_first()
            website = quote.css('div.travel-hotel.row div.hname.span6 div.row div.span5 p span a::text').extract_first()
            data = quote.css('div.travel-hotel.row div.hname.span6 div.row div.span5 p span::text').extract()
            # data = quote.css('div.travel-hotel.row div.hname.span6 div.row div.span5 p span::text').extract()
            phone_number = None
            mobile_number = None
            email = None
            classification = None
            grade = None
            for item in data:
                item = item.strip()
                if item.isdigit():
                    if item[:2] == '07':
                        mobile_number = item
                    else:
                        phone_number = item
                elif '+94' in item:
                    item = item.replace("+94", "0")
                    item = item.replace("-", "")
                    item = item.replace(" ", "")
                    if item[:2] == '07':
                        mobile_number = item
                    else:
                        phone_number = item
                elif '@' in item:
                    email = item
                elif len(item) == 1:
                    grade = item
                elif item != '' and item.isupper():
                    classification = item

            nameList = self.getNames()
            if not any(substring in name for substring in nameList):
                self.addName(name)
                yield {
                    'Name': name,
                    'Category': category,
                    'Classification': classification,
                    'Grade': grade,
                    'Capacity': capacity,
                    'Address': address,
                    'Telephone_Number': phone_number,
                    'Mobile_Phone_Number': mobile_number,
                    'Website': website,
                    'Email': email
                }


        next_page_list = response.css('div.links a ::attr(href)').extract()
        if next_page_list is not None:
            for page in next_page_list:
                scrape_list = self.getPages()
                if not any(substring in page for substring in scrape_list):
                    print("ADDING: "+page)
                    self.addPage(page)
                    if 'http' in page:
                        next_page = page
                    else:
                        next_page = response.urljoin(page)
                    yield scrapy.Request(next_page, callback=self.parse)
                # else:
                #     print("ALREADY EXISTS: " + page)