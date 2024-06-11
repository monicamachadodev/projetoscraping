import scrapy
import random
import time

class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    start_urls = ["https://lista.mercadolivre.com.br/tenis-de-corrida-feminino"]
    custom_settings = {
        'DOWNLOAD_DELAY': random.uniform(1, 3)  # Atraso de 1 a 3 segundos
    }
    page_count = 1
    max_page = 10

    def parse(self, response):
        # Verifica códigos de resposta HTTP
        if response.status in [403, 429, 503]:
            self.log(f'Banido! Código de resposta: {response.status}')
            return

        products = response.css('div.ui-search-result__content')

        for product in products:
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()
            yield {
                'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                'name': product.css('h2.ui-search-item__title::text').get(),
                'old_price_reais': prices[0] if len(prices) > 0 else None,
                'old_price_centavos': cents[0] if len(prices) > 0 else None,
                'new_price_reais': prices[1] if len(prices) > 1 else None,
                'new_price_centavos': cents[1] if len(prices) > 1 else None,
                'reviews_rating_number': product.css('span.ui-search-reviews__rating-number::text').get(),
                'reviews_amount': product.css('span.ui-search-reviews__amount::text').get(),
            }

        if self.page_count < self.max_page:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                time.sleep(random.uniform(1, 3))  # Atraso adicional para imitar comportamento humano
                yield response.follow(next_page, self.parse)
