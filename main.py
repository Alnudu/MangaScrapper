import os
from pickle import TRUE
import sys
import time
import webbrowser
import requests

from bs4 import BeautifulSoup as bs
from alive_progress import alive_bar


## CONFIGURACION ##
PATH_SAVE_DIR = "C:\MangaScrapper"
OPEN_BROWSER = True
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
        manga_links = soup.select("a.seriefs-link")
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


def manga_download(chapter):
    manga_chapters_imgs = []
    url = chapter
    img_number = 1
    try:
        r = requests.get(url)
        soup = bs(r.content, "html.parser")
        chapter_img = [img["src"] for img in soup.select(".reading-content img")]
        chapter_number = soup.find('h1').text
        title = soup.select_one(
        'div.entry-header:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > ol:nth-child(1) > li:nth-child(3) > a:nth-child(1)')
        chapter_title = title.text.strip()
    except:
        print ('La url que has introducido no parece correcta, por favor revísalo.')
        time.sleep(3)
        return
    else:
        print(f'Iniciando descarga de {chapter_number}')
    for img in chapter_img:
        manga_chapters_imgs.extend(chapter_img)
        try:
            os.makedirs(f'{PATH_SAVE_DIR}\{chapter_title}\{chapter_number}')
        except FileExistsError:
            pass
        with open(f'{PATH_SAVE_DIR}\{chapter_title}\{chapter_number}\{img_number}.jpg', 'wb') as file_handle:
            print(f'Descargando página {img_number} ...')
            file_handle.write(requests.get(img).content)
            file_handle.close()
            img_number = img_number + 1
    print(f'Capitulo {chapter_number} descargado .')
    time.sleep(3)
    return


def download_collection(chapter_index):
    try:
        get_manga_links(chapter_index)
        with alive_bar(len(manga_chapters_links)) as bar:
            for chapter in manga_chapters_links:
                manga_download(chapter)
                bar()
        manga_chapters_links.clear()
        print('Se han descargado todos lo capitulos disponibles.')
        return
    except:
        print ('La url que has introducido no parece correcta, por favor revísalo.')
        time.sleep(3)
        return


def get_manga_links(chapter_index):
    url = chapter_index
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    chapter_numbers = soup.select('div.chapter-link a')
    chapter_links = [manga_chapter['href'] for manga_chapter in chapter_numbers]
    manga_chapters_links.extend(reversed(chapter_links))
    return


LOGO = ''''                                                                                                                                                                                                                                                                      
███╗   ███╗ █████╗ ███╗   ██╗ ██████╗  █████╗     ███████╗ ██████╗██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
████╗ ████║██╔══██╗████╗  ██║██╔════╝ ██╔══██╗    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██╔████╔██║███████║██╔██╗ ██║██║  ███╗███████║    ███████╗██║     ██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██╔══██║    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗
██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝██║  ██║    ███████║╚██████╗██║  ██║██║  ██║██║     ██║     ███████╗██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝
'''''

def print_menu():
    print(LOGO)
    print('| https://www.manhwas.net | SCRAPPER')
    print(f'| Directorio de descargas | {PATH_SAVE_DIR}')
    print(f'| Navegador URL | {OPEN_BROWSER}')
    print(
        30 * "-", "MENU", 30 * "-")
    print("1. Modificar directorio de descargas.")
    print("2. Descargar un capitulo.")
    print("3. Descargar todos los capitulos.")
    print("4. Desactivar / Activar navegador URL.")
    print("5. Salir.")
    print(67 * "-")


LOOP = True

while LOOP:
    print_menu()
    choice = input("Introduce tu elección [1-5]: ")
    if choice == '1':
        print(f'Has seleccionado la opción {choice}.')
        print('Introduce tu ruta de descargas \nEjemplo C:\Descargas\Manga\ ')
        PATH_SAVE_DIR = input()
    elif choice == '2':
        print(f'Has seleccionado la opción {choice}.')
        print('Elige un capítulo manga de https://www.manhwas.net/ e introduce el enlace')
        print('Ejemplo "https://www.manhwas.net/leer/one-piece-1045.00"')
        print('Introduce la dirección URL del capítulo del manga:')
        if OPEN_BROWSER is True:
            webbrowser.open('https://www.manhwas.net/biblioteca?page=')
        chapter = input('URL ->')
        manga_download(chapter)
    elif choice == '3':
        print(f'Has seleccionado la opción {choice}.')
        print('Elige un manga de https://www.manhwas.net/ e introduce el enlace')
        print('Ejemplo "https://www.manhwas.net/manga/one-piece"')
        print('Introduce la dirección URL del manga:')
        if OPEN_BROWSER is True:
            webbrowser.open('https://www.manhwas.net/biblioteca?page=')
        chapter_index = input('URL ->')
        download_collection(chapter_index)
    elif choice == '4':
        print(f'Has seleccionado la opción {choice}.')
        if OPEN_BROWSER is True:
            OPEN_BROWSER = False
        else:
            OPEN_BROWSER = True
        print(f'Se ha configurado el navegador en {OPEN_BROWSER}.')
    elif choice == '5':
        sys.exit()
    else:
        print("Opción no válida, vuelve a intentarlo ..")

if __name__ == "__main__":
    print_menu()
    