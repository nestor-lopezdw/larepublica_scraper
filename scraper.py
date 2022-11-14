import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill[not(@class)]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice) # html donde podemos aplicar Xpath

            try:
                title = parsed.xpath(XPATH_TITLE)[0]  # traemos el primer elemento de la lista
                title = title.replace('\"', '')  # reemplaza comillas doble por nada, es decir, las elimina
                summary = parsed.xpath(XPATH_SUMMARY)[0]                
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            
            with open(f'{today}/{title}.txt', 'w',encoding='utf=8') as f: # with:  manejador contextual de Python, mantiene el archivo seguro en caso de fallos
                f.write(title)                
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL) #trae el cocumento html
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notices)
            today = datetime.date.today().strftime('%d-%m-%Y')  # guarda la fecha en formato dia mes año
            if not os.path.isdir(today):  # si existe una carpeta con el nombre de la fehca de hoy
                os.mkdir(today)                
            
            for link in links_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.estatus.code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__': #Se define el enterpoint
    run()

