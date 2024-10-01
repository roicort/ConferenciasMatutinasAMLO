import requests
from bs4 import BeautifulSoup
import html2text
from dateutil import parser
from fastprogress.fastprogress import master_bar, progress_bar

meses = {
    'enero': '01',
    'febrero': '02',
    'marzo': '03',
    'abril': '04',
    'mayo': '05',
    'junio': '06',
    'julio': '07',
    'agosto': '08',
    'septiembre': '09',
    'octubre': '10',
    'noviembre': '11',
    'diciembre': '12'
}

# Paso 1: Hacer una solicitud HTTP a la página web
url = 'https://www.gob.mx/presidencia/es/archivo/articulos?category=764&filter_origin=archive&idiom=es&order=DESC&page='


mb = master_bar(range(1, 258))

for i in mb:
    response = requests.get(url + str(i))
    soup = BeautifulSoup(response.content, 'html.parser')
    titulos = soup.find_all('h2')
    for j in progress_bar(range(len(titulos)), parent=mb):
        titulo = titulos[j]
        link = titulo.find('a')['href'][2:-2]
        article_url = 'https://www.gob.mx' + link
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        # Find tabindex="0"
        article = article_soup.find_all('div', {'tabindex': '0'})[0]
        title = article_soup.find('h1').text

        date_text = article_soup.find('p').text.split('|')[-1].strip()
        day, month_name, year = date_text.split(' de ')
        month = meses[month_name.lower()]
        formatted_date = f"{year}-{month}-{day.strip()}"

        title = title.replace('Versión estenográfica. ', '')

        markdown = html2text.html2text(article.prettify())
        with open(f'./corpus/{formatted_date}.md', 'w') as f:
            f.write(markdown)