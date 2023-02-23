import scrapy
import re
import pandas as pd

class AmericanasSpider(scrapy.Spider):
    name = "americanas"
    # Variável contadora para avançar as páginas
    cont = 0

    def start_requests(self):
        # Inícios das requisições
        self.items = []
        url = 'https://www.americanas.com.br/busca/' + self.produto.replace(' ', '-') + '?limit=24&offset=0'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # Localiza os produtos e seus respectivos atributos e anexa na lista de itens
        for produto in response.xpath('//div[contains(@class, "inStockCard__Wrapper")]'):
            preco = produto.xpath('.//span[contains(@class, "PromotionalPrice")]/text()').get()
            item = {
                'link_produto': 'https://www.americanas.com.br' + produto.xpath('.//a[contains(@class, "inStockCard__Link")]/@href').get(),
                'descricao_produto': produto.xpath('.//h3[contains(@class, "product-name")]/text()').get(),
                'preco_produto': re.sub('[^0-9,]', '', preco).replace(',', '.')
            }
            self.items.append(item)

        # Atualiza contador
        self.cont += 24

        ul = response.xpath('//ul[contains(@class, "src__Items")]').get()
        proxima_pagina = 'https://www.americanas.com.br/busca/' + self.produto.replace(' ', '-') + '?limit=24&offset=' + str(self.cont)

        # Avança para a próxima página
        if ul is not None:
            proxima_pagina = response.urljoin(proxima_pagina)
            yield scrapy.Request(proxima_pagina, callback=self.parse)

    # Salva os produtos encontrados em uma planilha Excel
    def closed(self, reason):
        filename = f"{self.name}.xlsx"
        df = pd.DataFrame(data=self.items)
        df.to_excel(filename)
