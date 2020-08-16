# Author: Darryl James
# Version: 15th August 2020
#
# This script takes the information from the top 1000 movies on
# IMDB at the time of running the script and 
# writes the data to a csv file.
#
# Resources / References: 
# Author: Angelica Dietzel
# Link: https://hackernoon.com/how-to-build-a-web-scraper-with-python-step-by-step-guide-jxkp3yum

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Initalize the arrays to store our information
class Movies:
    def __init__(self):
        self.titles = []
        self.years = []
        self.times = []
        self.ratings = []
        self.metascores = []
        self.votes = []
        self.gross = []

    def __str__(self):
        return "Title: %s | Year: %s | Runtime: %s | Rating: %s | Score: %s | Votes: %s | Gross: %s" \
               % (self.titles, self.years, self.times, self.ratings, self.metascores, self.votes, self.gross)

# The page number to parse through
count = 1

# Create the movies object to store our movie data
movies = Movies()

# Make the Data US Englsh
headers = {"Accept-Language" : "en-US, en;q=0.5"}

# Gather all top 1000 movies on IMDB 
while count != 1001:
    # The link to get the data from
    url = "https://www.imdb.com/search/title/?groups=top_1000&start=%d&ref_=adv_prv" % count

    # Get the contents of the link in US English
    results = requests.get(url, headers=headers)

    # Make the content easy to read/parse through
    soup = BeautifulSoup(results.text, "html.parser")
    listerItems = soup.find_all('div', class_='lister-item mode-advanced')

    for item in listerItems:
        # Find the title of the movie
        title = item.h3.a.text

        # Find the release year of the movie
        year = item.h3.find('span', class_='lister-item-year').text

        # Find the runtime of the movie if no time found it is -
        time = item.find('span', class_='runtime').text if item.find('span', class_='runtime') else '-'
        
        # Find the rating for the movie
        rating = float(item.strong.text)

        # Find the metascore for the movie if no score found it is 0
        score = item.find('span', class_='metascore').text if item.find('span', class_='metascore') else '0'
        
        # Find the votes and gross amount on the page 
        nv = item.find_all('span', attrs={'name' : 'nv'})
        votes = nv[0].text
        gross = nv[1].text if len(nv) > 1 else '-'

        # Add the variables to our Movies object respective lists
        movies.titles.append(title)
        movies.years.append(year)
        movies.times.append(time)
        movies.ratings.append(rating)
        movies.metascores.append(score)
        movies.votes.append(votes)
        movies.gross.append(gross)

    # Go to the next page
    count += 50

# The data frame that will contain the cleaned data for our movies
cleanedMovies = pd.DataFrame({
    'Movies' : movies.titles,
    'Year' : movies.years,
    'Runtime' : movies.times,
    'Imdb rating' : movies.ratings,
    'Metascores' : movies.metascores,
    'Votes' : movies.votes,
    'Gross (in millions)' : movies.gross,
})

# Clean the data and convert them to the right data type

# Find all the digits in the string and extract them as an int
cleanedMovies['Year'] = cleanedMovies['Year'].str.extract('(\d+)').astype(int)
cleanedMovies['Runtime'] = cleanedMovies['Runtime'].str.extract('(\d+)').astype(int)

# Extract the meta scores as an int
cleanedMovies['Metascores'] = cleanedMovies['Metascores'].astype(int)

# remove the extra commas and make the number an int
cleanedMovies['Votes'] = cleanedMovies['Votes'].str.replace(',', '').astype(int)

# Strip the $ from the left and the M from the right of the amount
cleanedMovies['Gross (in millions)'] = cleanedMovies['Gross (in millions)'].map(lambda x : x.lstrip('$').rstrip('M'))

# Convert the Gross values to floats if possible otherwise make them NaN
cleanedMovies['Gross (in millions)'] = pd.to_numeric(cleanedMovies['Gross (in millions)'], errors='coerce')

# Save the data to a csv file for later
cleanedMovies.to_csv('top1000Movies.csv')
