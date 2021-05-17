# Code by Dhruv
from bs4 import BeautifulSoup
import requests
import pandas as pd

captions = []

sites = [
    'https://imgflip.com/meme/Change-My-Mind', 
    'https://imgflip.com/memetemplate/Bernie-I-Am-Once-Again-Asking-For-Your-Support', 
    'https://imgflip.com/meme/Tuxedo-Winnie-The-Pooh',
    'https://imgflip.com/meme/One-Does-Not-Simply',
    'https://imgflip.com/meme/Surprised-Pikachu',
    'https://imgflip.com/meme/Laughing-Leo',
    'https://imgflip.com/meme/Spongebob-Ight-Imma-Head-Out',
    'https://imgflip.com/meme/216523697/All-My-Homies-Hate',
    'https://imgflip.com/meme/Sleeping-Shaq',
    'https://imgflip.com/meme/249257686/Bugs-bunny-communist'
    ]

data = []

for site in sites:
    for page in range(1, 1000):
        scrape = BeautifulSoup(requests.get(site + "?page=" + str(page)).text)
        memes = scrape.find_all("div", {"class": "base-unit clearfix"})
        if len(memes) == 0:
            continue
        for meme in memes:
            if meme.find("img") == None:
                continue
            if meme.find("img")['alt'] == None:
                continue
            if meme.find("img")['alt'].split("|") == None:
                continue
            caption = meme.find("img")['alt'].split("|")[1]
            data.append({"type": site.split("/")[4], "caption": caption.strip()})
        df = pd.DataFrame(data)
        df.to_csv('cap.csv', index=False)
