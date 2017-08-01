import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://www.chemistwarehouse.com.au/Shop-Online/81/Vitamins'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.css("#p_lt_ctl06_pageplaceholder_p_lt_ctl00_wPListC_lstElem td"):
            if item.css(".Save::text").extract():
                save=item.css(".Save::text").extract()[0][10:15]
            else:
                save=""
            # item= scrapy.Item()
            name = item.css(".product-name::text").extract()
            price = item.css(".Price::text").extract()[0][0:7]
            # item["save"] = save
            # return item
            # dic = {}

            yield {
                # dic[name:{'price':price,'save':save}]
                'name': name,
                'price': price,
                'save': save,
            }
        next_page  = response.css(".next-page::attr(href)").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)