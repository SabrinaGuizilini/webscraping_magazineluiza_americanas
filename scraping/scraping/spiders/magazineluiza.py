import scrapy
import re
import pandas as pd

class MagazineluizaSpider(scrapy.Spider):
    name = 'magazineluiza'
    # Variável contadora para avançar as páginas
    cont = 1

    def start_requests(self):
        # Inícios das requisições
        self.items = []
        url = 'https://www.magazineluiza.com.br/busca/'+self.produto.replace(' ', '+')+'/?page=1'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # Localiza os produtos e seus respectivos atributos e anexa na lista de itens
        for produto in response.xpath('//div[@data-testid="product-list"]/ul/li'):
            preco = produto.xpath('.//p[@data-testid="price-value"]/text()').get()
            item = {
                'link_produto': "https://www.magazineluiza.com.br"+produto.css('a::attr(href)').get(),
                'descricao_produto': produto.css('h2::text').get(),
                'preco_produto': re.sub('[^0-9,]', '', preco).replace(',', '.')
            }
            self.items.append(item)

        # Atualiza contador
        self.cont += 1

        icone_prox = response.xpath('//svg[@data-testid="ChevronRightIcon"]').get()
        proxima_pagina = 'https://www.magazineluiza.com.br/busca/'+self.produto.replace(' ', '+')+'/?page='+str(self.cont)

        # Avança para a próxima página
        if icone_prox is not None:
            proxima_pagina = response.urljoin(proxima_pagina)
            yield scrapy.Request(proxima_pagina, callback=self.parse)

    # Salva os produtos encontrados em uma planilha Excel
    def closed(self, reason):
        filename = f"{self.name}.xlsx"
        df = pd.DataFrame(data=self.items)
        df.to_excel(filename)
