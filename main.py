import requests
from bs4 import BeautifulSoup


### Put URLS of all albums you'd like to get lyrics for here.
### Or use the function getAlbumLyrics() in your own code.

URLS = []



def getMainPage(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def cleanTitle(title):
    title = title.text.strip()
    return title[:title.find('\n')]


def getSongTitlesAndLink(soup):
    job_elems = soup.find_all('div', class_='chart_row-content')
    titles = soup.find_all('h3', class_='chart_row-content-title')
    titles = [cleanTitle(title) for title in titles]
    links = [job.find('a')['href'] for job in job_elems]
    return dict(zip(titles, links))


def text_with_newlines(elem):
    text = ''
    for e in elem.descendants:
        if isinstance(e, str):
            text += e.strip()
        elif e.name == 'br' or e.name == 'p':
            text += '\n'
    return text

def getLyrics(url):
    soup = getMainPage(url)
    res=''
    try:
        # this might change over time! Check this code if errors arise.
        ress = soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-6 krDVEH')
        for re in ress:
            res += text_with_newlines(re)
    except IndexError:
        res += "Instrumental"
    return(res)


def getAlbum(url):
    mainPage = getMainPage(url)
    songs = getSongTitlesAndLink(mainPage)
    return {song: getLyrics(songs[song]) for song in songs}


def getAlbumLyrics(urls):
	with open('./lyrics.txt', 'w') as doc:
        for url in urls:
            album = getAlbum(url)
            print(url)
            for song in album:
                doc.write(song)
                doc.write('\n\n\n')
                doc.write(album[song])
                doc.write('\n\n\n')
            doc.write('\n\n\n\n\n\n\n\n')

def main():
    getAlbumLyrics(URLS)


if __name__ == '__main__':
    main()
