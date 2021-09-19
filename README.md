# mem2

Hi, ok here is the project:

The goal was to make a computer generate memes based on a variety of meme templates from imgflip.com >> https://imgflip.com/memegenerator

## Here are the templates we used: 

<img src="https://github.com/jacksonkunde/mem2/blob/main/Tuxedo-Winnie-The-Pooh.jpeg" width="200" height=auto>
    <p>Tuxedo Winnie The Pooh</p>
<img title="Surprised Pikachu" src="https://github.com/jacksonkunde/mem2/blob/main/Surprised-Pikachu.jpeg" width="200" height=auto>
    <p>Surprised Pikachu</p>
<img title="Laughing Leo" src="https://github.com/jacksonkunde/mem2/blob/main/Laughing-Leo.jpeg" width="200" height=auto>
    <p>Laughing Leo</p>
<img title="Change My Mind" src="https://github.com/jacksonkunde/mem2/blob/main/Change-My-Mind.jpeg" width="200" height=auto>
    <p>Change My Mind</p>
<img title="" src="https://github.com/jacksonkunde/mem2/blob/main/Sleeping-Shaq.jpeg" width="200" height=auto>
    <p>Sleeping Shaq</p>

With these templates we scraped https://imgflip.com/memegenerator to generate a csv of captions (this is done via scraper.py and the captions are contained in cap.csv)

Next, we trained one LSTM network for each template (this training is done in choo.py)

Then we developed code to generate a caption (from the trainied weights) and superimpose the text onto the template

Finally, we interfaced with the twitter API to directly post the memes.

Example memes can be found at https://twitter.com/AtcsMeme

Results: The LSTM generation isn't great, and doesn't mirror functional english well 
If we were given more time for this project we would scrape more data for each template and spend more time training. We are confident that with those steps the memery could be improved substantially.

-- Jackson Kunde
