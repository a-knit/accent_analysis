from bs4 import BeautifulSoup
import requests
from load_sound_data import load_sound
import os


def get_language_urls(index, language):
    urls_to_scrape = (index + 'browse_language.php?function=find&language=' + language)
    return urls_to_scrape

def get_speaker_urls(index, url, org_filter=None):
    
    def det_org(p):
        meta = str(p).split('</a>')[-1].strip('</p>')
        meta = meta.strip(',').split()
        return meta[-1]

    speaker_urls = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    content = soup.find(class_='content')
    for p in content.find_all('p'):
        if org_filter:
            org = det_org(p)
            if org==org_filter:
                speaker_urls.append(index + p.find('a')['href'])        
        else:
            speaker_urls.append(index + p.find('a')['href'])
    return speaker_urls

def get_audio(index, urls, language):
    audio = []
    for url in urls[300:]:
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
    os.chdir(directory)
    for mp3 in audio:
        fname = mp3.split('/')[-1]
        grabThis = 'wget '
        grabThis = grabThis + mp3
        os.system(grabThis)
    os.chdir('/Users/Alex/Documents/gitrepos/accent_analysis')

if __name__ == '__main__':
    index = 'http://accent.gmu.edu/'
    languages = ['english']
    for language in languages:
        urls_to_scrape = get_language_urls(index, language)
        speaker_urls = get_speaker_urls(index, urls_to_scrape, 'usa')
        get_audio(index, speaker_urls, language)
    