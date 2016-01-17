from bs4 import BeautifulSoup
import requests
import os
import re
import pandas as pd

def get_languages(url):
    results = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    for content in soup.find_all(class_='languagelist'):
        for a in content.find_all('a'):
            split1 = str(a).split('>')[1]
            split2 = split1.split('<')[0]
            results.append(split2)
    return results

def get_counts(url, languages):
    data = {}
    counts = []
    for language in languages:
        target = url + '?function=find&language=' + language
        r = requests.get(target)
        soup = BeautifulSoup(r.content)
        content = soup.find(class_='content')
        count = 0
        for p in content.find_all('p'):
            count += 1
        counts.append(count)
        print language, ' completed'
    data['language'] = languages
    data['count'] = counts
    return pd.DataFrame(data)

if __name__ == '__main__':
    index = 'http://accent.gmu.edu/browse_language.php'
    languages = get_languages(index)
    df = get_counts(index, languages)