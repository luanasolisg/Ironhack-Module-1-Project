import pandas as pd
import re
from functools import reduce
import requests
!pip install BeautifulSoup4
!pip install lxml
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

#Starting Web Scraping v1 PIB por pais

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita'
html = requests.get(url).content
html[0:500]
soup = BeautifulSoup(html, 'lxml')
table = soup.find_all('table',{'class':'wikitable sortable'})[0]
rows = table.find_all('tr')
rows_parsed = [row.text for row in rows]
def smart_parser(row_text):
    row_text = row_text.replace('\n\n', '\n').strip('\n')
    row_text = re.sub('\[\d\]', '', row_text)
    return list(map(lambda x: x.strip(), row_text.split('\n')))
well_parsed = list(map(lambda x: smart_parser(x), rows_parsed)
colnames = ['Rank',
  'Country',
  'GDP USD']
data = well_parsed[1:]
df1 = pd.DataFrame(data, columns=colnames)

#Starting Web Scraping v2 --> poblacion por país
url2 = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
html2 = requests.get(url2).content
html2[0:500]
soup2 = BeautifulSoup(html2, 'lxml')
# sortable table comes from inspecting the element on the web browser
table2 = soup2.find_all('table',{'class':'wikitable sortable mw-datatable'})[0]
# tr represent the table rows
rows2 = table2.find_all('tr')
rows_parsed2 = [row.text for row in rows2]
def smart_parser2(row_text):
    row_text = row_text.replace('\n\n', '\n').strip('\n')
    row_text = re.sub('\[\w\]', '', row_text)
    return list(map(lambda x: x.strip(), row_text.split('\n')))
well_parsed2 = list(map(lambda x: smart_parser2(x), rows_parsed2))
colnames2 = ['Rank',
  'Country',
  'Population',
  '% of World Population',
  'Date',
  'Source']
data2 = well_parsed2[1:245]
df2 = pd.DataFrame(data2, columns=colnames2)
df_scrap = [df2,df1]
#merge function:
def merge_df(list_df, column):
    return reduce(lambda left, right: pd.merge(left, right, on=column), list_df)
df_pop = merge_df (df_scrap , 'Country')
df_adding = df_pop[['Country','GDP USD','Population']]
df_union = [df_final,df_adding]
df_final2 = merge_df (df_union , 'Country')

#Top 20 countries with millionaire people
data_graph1 = df_final2.groupby('Country')['Name'].count().sort_values(ascending=False)[:20]
data_graph1.plot(kind='bar')
#Top 20 scountries by Worth sum
data_graph2 = df_final2.groupby('Country')['Worth(M.USD)'].sum().sort_values(ascending=False)[:20]
data_graph2.plot(kind='bar')
#Top 20 Sectors by Worth sum
data_graph2 = df_final2.groupby('Sector')['Worth(M.USD)'].sum().sort_values(ascending=False)[:20]
data_graph2.plot(kind='bar')
#Top 20 Sectors by companies count
data_graph2 = df_final2.groupby('Sector')['Company'].count().sort_values(ascending=False)[:20]
data_graph2.plot(kind='bar')