# Lexicanum-Scraper
This is a few files I had ChatGPT write up.
The goal was to get an oversight of all the space marine chapters with an offical colour scheme.

The data was found/taken from [The Community Created Warhammer 40,000 Encyclopedia: https://wh40k.lexicanum.com](https://wh40k.lexicanum.com/wiki/Main_Page)
Massive props to the team and contributors for getting these images, as otherwise I couldn't do this.

And yes, I could've written this myself to learn a new skill. But honestly? This was made at 1AM with a semi joke-purpose to see if I can paint all the official chapters.<br>
This has gotten me a bit more interested in webscrapers and webscraping etiquette, so who knows for a future project?

# Requirements
Not sure, just used ```Python filename.py``` on my Fedora 42 + KDE Plasma 6.13 install.
Python version is 3.13.7

# getMarines.py
Outputs a big list of every marine chapter with a valid URL from the main list.

# Lexicanum_scraper_v2.py
Checks a file named urls.csv ```note, first row and column has to be URL. URLS must be in column that has URL in row 1.```
Checks the infobox, if all3 images are unknown, we state is has no scheme.
If no infobox, we state it has no infobox
If there is an image, we check if there is anymore and write all of them to csv
Outputs CSV

# Disclaimer
These are webscrapers written by AI, they try to be considerate. But I don't know alot about scraping etiquette.
Don't abuse/spam these files or the Lexicanum. They are cool people doing something for the love of the game. Leave em be.
