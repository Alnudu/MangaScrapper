import requests
from bs4 import BeautifulSoup as bs
import os

## CONFIGURACION ##
path_save_dir = "C:\LOL"  # Ejemplo de ruta c:\test
## ARRAYS COMUNES ##
manga_chapters_links = []


def manga_site_scan():
    page = 1
    all_manga_titles = []
    all_manga = []
    all_manga_links = []
    while page != 44:
        url = f'https://www.manhwas.net/biblioteca?page={page}'
        r = requests.get(url)
        soup = bs(r.content, "html.parser")
        manga_titles = soup.select("h5.series-title")
        manga_links = soup.select("a.series-link")
        manga_links_ref = [manga_link['href'] for manga_link in manga_links]
        for titles in manga_titles:
            f = open("mangas.txt", "a")
            f.write(f'{titles.get_text()}')
            print(titles.get_text())
            all_manga_titles.extend(titles)
            all_manga_links.extend(manga_links_ref)
        page = page + 1
        print(page)
    for element in all_manga_titles:
        all_manga.append(element.strip())
    return


def manga_chapter_index(chapter_index):
    url = chapter_index
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    chapter_numbers = soup.select('div.chapter-link a')
    chapter_links = [manga_chapter['href'] for manga_chapter in chapter_numbers]
    manga_chapters_links.extend(reversed(chapter_links))
    return

def manga_download(chapter):
    manga_chapters_imgs = []
    url = chapter
    img_number = 1
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    chapter_img = [img["src"] for img in soup.select(".reading-content img")]
    chapter_number = soup.find('h1').text
    title = soup.select_one(
        'div.entry-header:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > ol:nth-child(1) > li:nth-child(3) > a:nth-child(1)')
    chapter_title = title.text.strip()
    for img in chapter_img:
        manga_chapters_imgs.extend(chapter_img)
        try:
            os.makedirs(f'{path_save_dir}\{chapter_title}\{chapter_number}')
        except FileExistsError:
            pass
        f = open(f'{path_save_dir}\{chapter_title}\{chapter_number}\{img_number}.jpg', 'wb')
        print(f'Descargando página {img_number} ...')
        img_number = img_number + 1
        f.write(requests.get(img).content)
        f.close()
    print(f'Capitulo {chapter_number} descargado .')
    return


def download_collection(chapter_index):
    manga_chapter_index(chapter_index)
    for chapter in manga_chapters_links:
        manga_download(chapter)
    # Limpiamos los arrays al terminar el bucle.
    manga_chapters_links.clear()
    print('Se han descargado todos lo capitulos disponibles.')
    return


## Interfaz ##
print('Para descargar una colección de manga es necesario que introduzcas la url:')
chapter_index = input()
download_collection(chapter_index)