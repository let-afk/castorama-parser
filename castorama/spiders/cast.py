import scrapy
from scrapy.http import HtmlResponse
from castorama.items import CastoramaItem
from scrapy.loader import ItemLoader

class CastSpider(scrapy.Spider):
    name = "cast"
    allowed_domains = ["castorama.ru"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('search_item')}"]

    def parse(self, response, **kwargs):
        links = response.xpath("//a[@class='product-card__img-link']")
        if links:
            for link in links:
                yield response.follow(link, callback=self.parse_item)
        next_page = response.xpath("//a[@title='След.']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
    @staticmethod
    def parse_item(response: HtmlResponse):

        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', "//span[@class='price']//text()")
        loader.add_xpath('currency', "//span[@class='currency']//text()")
        # //div[contains(@class, 'product-media__top')]/ul//img
        loader.add_xpath('photos', "//div[contains(@class,'product-media__top')]/ul//img[1]/@src | //div[contains(@class,'product-media__top')]/ul//img[1]/@data-src")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # name = response.xpath("//h1/text()").get()
        # price = response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").get()
        # author = response.xpath("//a[contains(@href,'/author/')]/text()").get()
        # photos = response.xpath("//picture[@class='product-poster__main-picture']/source[1]/@srcset | "
        #                         "//picture[@class='product-poster__main-picture']/source[1]/@data-srcset").getall()
        # url = response.url
        #
        # yield BookparserItem(name=name, price=price, author=author, photos=photos, url=url)
