# top1000_imdb_scraper
A web scraper which takes the current top 1000 movies on IMDB and writes the data about them to a csv file.

## Data Included

* Movie Title
* Year of Release
* Runtime in minutes
* IMDB Rating
* Metascore
* Votes
* Gross in millions

### Some Issues

* Movies with metascores of 0 originally had no metascores and as such 0 is the placeholder value for them.
* Like most times you web scrape, not all the slots will have values in them since not all the movies report some of the metrics I was lookiing for.
