import pandas as pd
import re
import os
import requests
from bs4 import BeautifulSoup

def find_title(url):
    '''
    This function extracts the name of the episode from the URL.
    '''
    match = re.search(r'/wiki/([^/]+)$', url)
    title = match.group(1).replace('_', ' ')
    if '(Black Mirror)' in title:
        return title.replace('(Black Mirror)', '').strip()
    else:
        return title

def generate_text(season):
    '''
    This function scrapes the Wikipedia page for each episode of the season and puts them in a dictionary.
    '''
    dict = {}
    for episode in season:
        request = requests.get(episode)
        wiki_page = BeautifulSoup(request.text, 'html.parser')

        lst = []

        for paragraph in wiki_page.select('p'):
            lst.append(paragraph.getText())
        
        title = find_title(episode)
        text = "\n".join(lst)
        dict[title] = text
    return dict

def generate_df(season):
    '''
    This function generates df for the season/special/interactive film.
    '''
    data = {
        'Episode':generate_text(season).keys(),
        'Text':generate_text(season).values()
    }

    df = pd.DataFrame(data)
    return df

s1 = [
    'https://en.wikipedia.org/wiki/The_National_Anthem_(Black_Mirror)',
    'https://en.wikipedia.org/wiki/Fifteen_Million_Merits',
    'https://en.wikipedia.org/wiki/The_Entire_History_of_You'
]

s2 = [
    'https://en.wikipedia.org/wiki/Be_Right_Back',
    'https://en.wikipedia.org/wiki/White_Bear_(Black_Mirror)',
    'https://en.wikipedia.org/wiki/The_Waldo_Moment'
]

special = ['https://en.wikipedia.org/wiki/White_Christmas_(Black_Mirror)']

s3 = [
    'https://en.wikipedia.org/wiki/Nosedive_(Black_Mirror)',
    'https://en.wikipedia.org/wiki/Playtest_(Black_Mirror)',
    'https://en.wikipedia.org/wiki/Shut_Up_and_Dance_(Black_Mirror)',
    'https://en.wikipedia.org/wiki/San_Junipero',
    'https://en.wikipedia.org/wiki/Men_Against_Fire',
    'https://en.wikipedia.org/wiki/Hated_in_the_Nation'
]

s4 = [
    'https://en.wikipedia.org/wiki/USS_Callister',
    'https://en.wikipedia.org/wiki/Arkangel_(Black_Mirror)',
    'https://en.wikipedia.org/wiki/Crocodile_(Black_Mirror)',
    'https://en.wikipedia.org/wiki/Hang_the_DJ',
    'https://en.wikipedia.org/wiki/Metalhead_(Black_Mirror)',
    'https://en.wikipedia.org/wiki/Black_Museum_(Black_Mirror)'
]

interactive_film = ['https://en.wikipedia.org/wiki/Black_Mirror:_Bandersnatch']

s5 = [
    'https://en.wikipedia.org/wiki/Striking_Vipers',
    'https://en.wikipedia.org/wiki/Smithereens_(Black_Mirror)',
    'https://en.wikipedia.org/wiki/Rachel,_Jack_and_Ashley_Too'
]

s6 = [
    'https://en.wikipedia.org/wiki/Joan_Is_Awful',
    'https://en.wikipedia.org/wiki/Loch_Henry',
    'https://en.wikipedia.org/wiki/Beyond_the_Sea_(Black_Mirror)',
    'https://en.wikipedia.org/wiki/Mazey_Day_(Black_Mirror)',
    'https://en.wikipedia.org/wiki/Demon_79',
      ]

list_of_seasons = [s1, s2, special, s3, s4, interactive_film, s5, s6]
str_of_seasons = ['s1', 's2', 'special', 's3', 's4', 'interactive_film', 's5', 's6']

directory_path = 'data'

for i in range(len(list_of_seasons)):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_path = os.path.join(directory_path, str_of_seasons[i] + '.csv')
    df = generate_df(list_of_seasons[i])
    df.to_csv(file_path, index=False)
