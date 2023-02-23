from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraping.spiders.magazineluiza import MagazineluizaSpider
from scraping.spiders.americanas import AmericanasSpider

import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Entrada
nome_produto = input('Entre com o nome do produto: ')


# Execução das Spiders
settings = get_project_settings()
process = CrawlerProcess(settings)

magazineluiza_crawler = MagazineluizaSpider
americanas_crawler = AmericanasSpider

process.crawl(magazineluiza_crawler, produto=nome_produto)
process.crawl(americanas_crawler, produto=nome_produto)

process.start()

# Captura de dados relevantes nas planilhas
magazineluiza_df = pd.read_excel('magazineluiza.xlsx')

total_prod_magazineluiza = magazineluiza_df['preco_produto'].count()
media_prod_magazineluiza = magazineluiza_df['preco_produto'].mean()

indice_do_maior_preco_magazineluiza = magazineluiza_df['preco_produto'].idxmax()
descricao_do_maior_preco_magazineluiza = magazineluiza_df.loc[indice_do_maior_preco_magazineluiza, 'descricao_produto']
link_do_maior_preco_magazineluiza = magazineluiza_df.loc[indice_do_maior_preco_magazineluiza, 'link_produto']
maior_preco_magazineluiza = magazineluiza_df.loc[indice_do_maior_preco_magazineluiza, 'preco_produto']

indice_do_menor_preco_magazineluiza = magazineluiza_df['preco_produto'].idxmin()
descricao_do_menor_preco_magazineluiza = magazineluiza_df.loc[indice_do_menor_preco_magazineluiza, 'descricao_produto']
link_do_menor_preco_magazineluiza = magazineluiza_df.loc[indice_do_menor_preco_magazineluiza, 'link_produto']
menor_preco_magazineluiza = magazineluiza_df.loc[indice_do_menor_preco_magazineluiza, 'preco_produto']

americanas_df = pd.read_excel('americanas.xlsx')

total_prod_americanas = americanas_df['preco_produto'].count()
media_prod_americanas = americanas_df['preco_produto'].mean()

indice_do_maior_preco_americanas = americanas_df['preco_produto'].idxmax()
descricao_do_maior_preco_americanas = americanas_df.loc[indice_do_maior_preco_americanas, 'descricao_produto']
link_do_maior_preco_americanas = americanas_df.loc[indice_do_maior_preco_americanas, 'link_produto']
maior_preco_americanas = americanas_df.loc[indice_do_maior_preco_americanas, 'preco_produto']

indice_do_menor_preco_americanas = americanas_df['preco_produto'].idxmin()
descricao_do_menor_preco_americanas = americanas_df.loc[indice_do_menor_preco_americanas, 'descricao_produto']
link_do_menor_preco_americanas = americanas_df.loc[indice_do_menor_preco_americanas, 'link_produto']
menor_preco_americanas = americanas_df.loc[indice_do_menor_preco_americanas, 'preco_produto']

# Relatório geral da busca
print('Relatório de busca - ' + nome_produto)

print('\nMagazine Luiza:')
print('-> Total de produtos: '+ str(total_prod_magazineluiza))
print(f'-> Média dos preços: R${media_prod_magazineluiza:.2f}')
print('-> Produto mais barato:')
print('\t-> Descrição: '+ descricao_do_menor_preco_magazineluiza)
print('\t-> Preço: R$'+ str(menor_preco_magazineluiza))
print('\t-> Link: '+ link_do_menor_preco_magazineluiza)
print('-> Produto mais caro:')
print('\t-> Descrição: '+ descricao_do_maior_preco_magazineluiza)
print('\t-> Preço: R$'+ str(maior_preco_magazineluiza))
print('\t-> Link: '+ link_do_maior_preco_magazineluiza)

print('\nAmericanas:')
print('-> Total de produtos: '+ str(total_prod_americanas))
print(f'-> Média dos preços: R${media_prod_americanas:.2f}')
print('-> Produto mais barato:')
print('\t-> Descrição: '+ descricao_do_menor_preco_americanas)
print('\t-> Preço: R$'+ str(menor_preco_americanas))
print('\t-> Link: '+ link_do_menor_preco_americanas)
print('-> Produto mais caro:')
print('\t-> Descrição: '+ descricao_do_maior_preco_americanas)
print('\t-> Preço: R$'+ str(maior_preco_americanas))
print('\t-> Link: '+ link_do_maior_preco_americanas)

# Geração de gráficos comparativos com Plotly
fig = make_subplots(
    rows=2, cols=2, subplot_titles=("Total de Produtos", "Média dos Preços", "Valor do Menor Preço", "Valor do Maior Preço")
)

fig.add_trace(go.Bar(x=['Magazine Luiza', 'Americanas'], y=[total_prod_magazineluiza, total_prod_americanas], name='Total de Produtos'), row=1, col=1)
fig.add_trace(go.Bar(x=['Magazine Luiza', 'Americanas'], y=[media_prod_magazineluiza, media_prod_americanas], name='Média dos Preços'), row=1, col=2)
fig.add_trace(go.Bar(x=['Magazine Luiza', 'Americanas'], y=[menor_preco_magazineluiza, menor_preco_americanas], name='Valor do Menor Preço'), row=2, col=1)
fig.add_trace(go.Bar(x=['Magazine Luiza', 'Americanas'], y=[maior_preco_magazineluiza, maior_preco_americanas], name='Valor do Maior Preço'), row=2, col=2)

fig.update_layout(title_text="Gráficos Comparativos", height=700)
fig.show()