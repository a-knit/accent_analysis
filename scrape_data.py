from bs4 import BeautifulSoup
import requests
from load_sound_data import load_sound
import os


def get_language_urls(index, language):
    urls_to_scrape = (index + 'browse_language.php?function=find&language=' + language)
    return urls_to_scrape

def get_speaker_urls(index, url):
    speaker_urls = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    content = soup.find(class_='content')
    for a in content.find_all('a'):
        speaker_urls.append(index + a['href'])
    return speaker_urls

def get_audio(index, urls, language):
    audio = []
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        content = soup.find(class_='content')
        source = soup.find('source')['src']
        source = source.split('/')
        source = index + source[-2] + '/' + source[-1]
        audio.append(source)
    directory = 'files/' + language + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for mp3 in audio:
        fname = mp3.split('/')[-1]
        with open(directory + fname, 'wb') as f:
            print 'Writing file - ', mp3
            f.write(r)

if __name__ == '__main__':
    index = 'http://accent.gmu.edu/'
    languages = ['hindi']
    for language in languages:
        urls_to_scrape = get_language_urls(index, language)
        speaker_urls = get_speaker_urls(index, urls_to_scrape)
        get_audio(index, speaker_urls, language)
    