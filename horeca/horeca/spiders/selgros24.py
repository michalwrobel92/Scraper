import scrapy
from horeca.items import ShopProduct


class Selgros24Spider(scrapy.Spider):
    name = "selgros24spider"
    allowed_domains = ["selgros24.pl"]
    start_urls = ["https://selgros24.pl/artykuly-spozywcze-pc1160.html"]

    def parse(self, response, **kwargs):
        products = response.css('.small-product')

        product_item = ShopProduct()

        for product in products:

            product_item['name'] = product.css('.product-name>a::text').get(),
            product_item['price'] = product.css('.actual-price').get().replace('<div class="actual-price">', '').replace(
                    '<span class="upper-index">', '').replace('</span>', '').replace('</div>', '').replace(
                    '<div class="actual-price as-second">', ''),
            product_item['url'] = product.css('h2.product-name a').attrib['href']
            yield product_item

        next_page = response.css('li.nextPageFooter > a::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://selgros24.pl/artykuly-spozywcze-pc1160.html' + next_page
            yield response.follow(next_page_url, callback=self.parse)